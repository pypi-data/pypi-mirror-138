#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This program runs the model defined by the user.

Author: Farid Mohammadi, M.Sc.
E-Mail: farid.mohammadi@iws.uni-stuttgart.de
Department of Hydromechanics and Modelling of Hydrosystems (LH2)
Institute for Modelling Hydraulic and Environmental Systems (IWS), University
of Stuttgart, www.iws.uni-stuttgart.de/lh2/
Pfaffenwaldring 61
70569 Stuttgart

Created in July 2019

"""

import os
import shutil
import h5py
import numpy as np
import time
import zipfile
import pandas as pd
from functools import reduce
import multiprocessing
import tqdm


class PyLinkForwardModel(object):
    """A forward model binder
    This calss serves as a code wrapper. This wrapper allows the execution of
        a third-party software/solver within the scope of BayesValidRox.
    The wrapper provides two options:
        1) link_type='PyLink':
            Runs the third-party software using a sell command with given input
            files.
        2) link_type='function':
            For this case, it is assumed that model can be run using a function
            written separately in a Python script. This function recieves the
            parameters in an array of shape (n_samples, n_params) and returns
            a dictionary with the x_values and output arrays for given output
            names.
    """

    def __init__(self, link_type='PyLink', name=None, shell_command='',
                 py_file=None, input_file=None, input_template=None,
                 aux_file=None, exe_path='', multi_process=True, n_cpus=None,
                 output_parser='', output_names=[], output_file_names=[],
                 meas_file=None, meas_file_valid=None, mc_ref_file=None,
                 obs_dict={}, obs_dict_valid={}, mc_ref_dict={}):
        self.link_type = link_type
        self.name = name
        self.shell_command = shell_command
        self.py_file = py_file
        self.input_file = input_file
        self.input_template = input_template
        self.aux_file = aux_file
        self.exe_path = exe_path
        self.multi_process = multi_process
        self.n_cpus = n_cpus
        self.Output.parser = output_parser
        self.Output.names = output_names
        self.Output.file_names = output_file_names
        self.meas_file = meas_file
        self.meas_file_valid = meas_file_valid
        self.mc_ref_file = mc_ref_file
        self.observations = obs_dict
        self.observations_valid = obs_dict_valid
        self.mc_reference = mc_ref_dict

    # Nested class
    class Output:
        def __init__(self):
            self.parser = None
            self.names = None
            self.file_names = None

    # -------------------------------------------------------------------------
    def within_range(self, out, minout, maxout):
        inside = False
        if (out > minout).all() and (out < maxout).all():
            inside = True
        return inside

    # -------------------------------------------------------------------------
    def read_observation(self, case='calib'):
        """
        Reads/prepare the observation/measurement data for
        calibration.

        Returns
        -------
        DataFrame
            A dataframe with the calibration data.

        """
        if case.lower() == 'calib':
            if hasattr(self, 'observations') and \
               isinstance(self.observations, dict):
                obs = pd.DataFrame.from_dict(self.observations)
            elif hasattr(self, 'observations'):
                FilePath = os.path.join(os.getcwd(), self.meas_file)
                obs = pd.read_csv(FilePath, delimiter=',')
            else:
                raise Exception("Please provide the observation data as a "
                                "dictionary via observations attribute or pass"
                                " the csv-file path to MeasurementFile "
                                "attribute")
        elif case.lower() == 'valid':
            if hasattr(self, 'observations_valid') and \
               isinstance(self.observations_valid, dict):
                obs = pd.DataFrame.from_dict(self.observations_valid)
            elif hasattr(self, 'observations_valid'):
                FilePath = os.path.join(os.getcwd(), self.meas_file_valid)
                obs = pd.read_csv(FilePath, delimiter=',')
            else:
                raise Exception("Please provide the observation data as a "
                                "dictionary via Observations attribute or pass"
                                " the csv-file path to MeasurementFile "
                                "attribute")

        # Compute the number of observation
        nObs = reduce(lambda x, y: x*y, obs[self.Output.names].shape)

        if case.lower() == 'calib':
            self.observations = obs
            self.nObs = nObs
            return self.observations
        elif case.lower() == 'valid':
            self.observations_valid = obs
            self.nObsValid = nObs
            return self.observations_valid

    # -------------------------------------------------------------------------
    def read_mc_reference(self):
        """
        Is used, if a Monte-Carlo reference is available for
        further in-depth post-processing after meta-model training.

        Returns
        -------
        None

        """
        if hasattr(self, 'mc_reference') and \
           isinstance(self.mc_reference, dict):
            self.mc_reference = pd.DataFrame.from_dict(self.mc_reference)
        elif hasattr(self, 'mc_reference'):
            FilePath = os.path.join(os.getcwd(), self.mc_ref_file)
            self.mc_reference = pd.read_csv(FilePath, delimiter=',')
        else:
            raise Exception("Please provide the MC reference data as a "
                            "dictionary via mc_reference attribute or pass the"
                            " csv-file path to mc_ref_file attribute")
        return self.mc_reference

    # -------------------------------------------------------------------------
    def read_output(self):
        """
        Reads the the parser output file and returns it as an
         executable function. It is required when the models returns the
         simulation outputs in csv files.

        Returns
        -------
        Output : func
            Output parser function.

        """
        output_func_name = self.Output.parser

        output_func = getattr(__import__(output_func_name), output_func_name)

        file_names = []
        for File in self.Output.file_names:
            file_names.append(os.path.join(self.exe_path, File))
        try:
            output = output_func(self.name, file_names)
        except TypeError:
            output = output_func(file_names)
        return output

    # -------------------------------------------------------------------------
    def update_input_params(self, new_input_file, param_sets):
        """
        Finds this pattern with <X1> in the new_input_file and replace it with
         the new value from the array param_sets.

        Parameters
        ----------
        new_input_file : TYPE
            DESCRIPTION.
        param_sets : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        NofPa = param_sets.shape[0]
        text_to_search_list = [f'<X{i+1}>' for i in range(NofPa)]

        for filename in new_input_file:
            # Read in the file
            with open(filename, 'r') as file:
                filedata = file.read()

            # Replace the target string
            for text_to_search, params in zip(text_to_search_list, param_sets):
                filedata = filedata.replace(text_to_search, f'{params:0.4e}')

            # Write the file out again
            with open(filename, 'w') as file:
                file.write(filedata)

    # -------------------------------------------------------------------------
    def run_command(self, command, output_file_names):
        """
        Runs the execution command given by the user to run the given model.
        It checks if the output files have been generated. If yes, the jobe is
         done and it extracts and returns the requested output(s). Otherwise,
         it executes the command again.

        Parameters
        ----------
        command : string
            The command to be executed.
        output_file_names : list
            Name of the output file names.

        Returns
        -------
        simulation_outputs : array of shape (n_obs, n_outputs)
            Simulation outputs.

        """

        # Check if simulation is finished
        while True:
            time.sleep(3)
            files = os.listdir(".")
            if all(elem in files for elem in output_file_names):
                break
            else:
                # Run command
                Process = os.system(f'./../{command}')
                if Process != 0:
                    print('\nMessage 1:')
                    print(f'\tIf value of \'{Process}\' is a non-zero value, '
                          'then compilation problems \n' % Process)

        os.chdir("..")

        # Read the output
        simulation_outputs = self.read_output()

        return simulation_outputs

    # -------------------------------------------------------------------------
    def run_forwardmodel(self, xx):
        """
        This function creates subdirectory for the current run and copies the
        necessary files to this directory and renames them. Next, it executes
        the given command.
        """
        CollocationPoints, Run_No, keyString = xx

        # Handle if only one imput file is provided
        if not isinstance(self.input_template, list):
            self.input_template = [self.input_template]
        if not isinstance(self.input_file, list):
            self.input_file = [self.input_file]

        NewInputfile = []
        # Loop over the InputTemplates:
        for InputTemplate in self.input_template:
            if '/' in InputTemplate:
                InputTemplate = InputTemplate.split('/')[-1]
            NewInputfile.append(InputTemplate.split('.tpl')[0] + keyString +
                                f"_{Run_No+1}" +
                                InputTemplate.split('.tpl')[1])

        # Create directories
        newpath = self.name + keyString + f'_{Run_No+1}'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        # Copy the necessary files to the directories
        for InputTemplate in self.input_template:
            # Input file(s) of the model
            shutil.copy2(InputTemplate, newpath)
        # Auxiliary file
        if self.aux_file is not None:
            shutil.copy2(self.aux_file, newpath)  # Auxiliary file

        # Rename the Inputfile and/or auxiliary file
        os.chdir(newpath)
        for input_tem, input_file in zip(self.input_template, NewInputfile):
            if '/' in InputTemplate:
                input_tem = input_tem.split('/')[-1]
            os.rename(input_tem, input_file)

        # Update the parametrs in Input file
        self.update_input_params(NewInputfile, CollocationPoints)

        # Update the user defined command and the execution path
        try:
            NewCommand = self.shell_command .replace(self.input_file[0],
                                                     NewInputfile[0]).replace(
                                                         self.input_file[1],
                                                         NewInputfile[1])
        except:
            NewCommand = self.shell_command.replace(self.input_file[0],
                                                    NewInputfile[0])

        OutputFileNames = self.Output.file_names
        self.exe_path = os.getcwd()

        # Run the model
        Output = self.run_command(NewCommand, OutputFileNames)

        return Output

    # -------------------------------------------------------------------------
    def run_model_parallel(self, c_points, prevRun_No=0, keyString='',
                           mp=True):
        """
        Runs model simulations. If mp is true (default), then the simulations
         are started in parallel.

        Parameters
        ----------
        c_points : array like of shape (n_samples, n_params)
            Collocation points (training set).
        prevRun_No : int, optional
            Previous run number, in case the sequential design is selected.
            The default is 0.
        keyString : string, optional
            A descriptive string for validation runs. The default is ''.
        mp : bool, optional
            Multiprocessing. The default is True.

        Returns
        -------
        all_outputs : dict
            A dictionary with x values (time step or point id) and all outputs.
            Each key contains an array of the shape (n_samples, n_obs).
        new_c_points : array
            Updated collocation points (training set). If a simulation does not
            executed successfully, the parameter set is removed.

        """

        # Create hdf5 metadata
        hdf5file = 'ExpDesign'+'_'+self.name+'.hdf5'
        hdf5_exist = os.path.exists(hdf5file)
        file = h5py.File(hdf5file, 'a')

        # Initilization
        P = len(c_points)
        OutputNames = self.Output.names
        self.NofVar = len(OutputNames)
        all_outputs = {}

        # Extract the function
        if self.link_type.lower() == 'function':
            # Prepare the function
            Function = getattr(__import__(self.py_file), self.py_file)
        # ---------------------------------------------------------------
        # -------------- Multiprocessing with Pool Class ----------------
        # ---------------------------------------------------------------
        # Start a pool with the number of CPUs
        if self.n_cpus is None:
            nrCPUs = multiprocessing.cpu_count()
        else:
            nrCPUs = self.n_cpus

        # Run forward model either normal or with multiprocessing
        if not self.multi_process:
            group_results = list([self.run_forwardmodel((c_points,
                                                         prevRun_No,
                                                         keyString))])
        else:
            with multiprocessing.Pool(nrCPUs) as p:
                desc = f'Running forward model {keyString}'
                if self.link_type.lower() == 'function':
                    imap_var = p.imap(Function, c_points[:, np.newaxis])
                else:
                    imap_var = p.imap(self.run_forwardmodel,
                                      zip(c_points,
                                          [prevRun_No+i for i in range(P)],
                                          [keyString]*P))

                group_results = list(tqdm.tqdm(imap_var, total=P, desc=desc))

        # Save time steps or x-values
        x_values = group_results[0][0]
        all_outputs["x_values"] = x_values
        if not hdf5_exist:
            if type(x_values) is dict:
                grp_x_values = file.create_group("x_values/")
                for varIdx, var in enumerate(OutputNames):
                    grp_x_values.create_dataset(var, data=x_values[var])
            else:
                file.create_dataset("x_values", data=x_values)

        # save each output in their corresponding array
        NaN_idx = []
        for varIdx, var in enumerate(OutputNames):

            if not hdf5_exist:
                grpY = file.create_group("EDY/"+var)
            else:
                grpY = file.get("EDY/"+var)

            Outputs = np.asarray([item[varIdx+1] for item in group_results],
                                 dtype=np.float64)

            if prevRun_No == 0 and keyString == '':
                grpY.create_dataset(f'init_{keyString}', data=Outputs)
            else:
                try:
                    oldEDY = np.array(file[f'EDY/{var}/adaptive_{keyString}'])
                    del file[f'EDY/{var}/adaptive_{keyString}']
                    data = np.vstack((oldEDY, Outputs))
                except KeyError:
                    data = Outputs
                grpY.create_dataset('adaptive_'+keyString, data=data)

            NaN_idx = np.unique(np.argwhere(np.isnan(Outputs))[:, 0])
            all_outputs[var] = np.delete(Outputs, NaN_idx, axis=0)

            if prevRun_No == 0 and keyString == '':
                grpY.create_dataset(f"New_init_{keyString}",
                                    data=all_outputs[var])
            else:
                try:
                    name = f'EDY/{var}/New_adaptive_{keyString}'
                    oldEDY = np.array(file[name])
                    del file[f'EDY/{var}/New_adaptive_{keyString}']
                    data = np.vstack((oldEDY, all_outputs[var]))
                except KeyError:
                    data = all_outputs[var]
                grpY.create_dataset(f'New_adaptive_{keyString}', data=data)

        # Print the collocation points whose simulations crashed
        if len(NaN_idx) != 0:
            print('\n')
            print('*'*20)
            print("\nThe following parametersets have been removed:\n",
                  c_points[NaN_idx])
            print("\n")
            print('*'*20)

        # Pass it to the attribute
        new_c_points = np.delete(c_points, NaN_idx, axis=0)
        self.OutputMatrix = all_outputs

        # Save CollocationPoints
        grpX = file.create_group("EDX") if not hdf5_exist else file.get("EDX")
        if prevRun_No == 0 and keyString == '':
            grpX.create_dataset("init_"+keyString, data=c_points)
            if len(NaN_idx) != 0:
                grpX.create_dataset("New_init_"+keyString, data=new_c_points)

        else:
            try:
                name = f'EDX/adaptive_{keyString}'
                oldCollocationPoints = np.array(file[name])
                del file[f'EDX/adaptive_{keyString}']
                data = np.vstack((oldCollocationPoints, new_c_points))
            except KeyError:
                data = new_c_points
            grpX.create_dataset('adaptive_'+keyString, data=data)

            if len(NaN_idx) != 0:
                try:
                    name = f'EDX/New_adaptive_{keyString}'
                    oldCollocationPoints = np.array(file[name])
                    del file[f'EDX/New_adaptive_{keyString}']
                    data = np.vstack((oldCollocationPoints, new_c_points))
                except KeyError:
                    data = new_c_points
                grpX.create_dataset('New_adaptive_'+keyString, data=data)

        # Close h5py file
        file.close()

        return all_outputs, new_c_points

    # -------------------------------------------------------------------------
    def zip_subdirs(self, dir_name, key):
        """
        Zips all the files containing the key(word).

        Parameters
        ----------
        dir_name : string
            Directory name.
        key : string
            Keyword to search for.

        Returns
        -------
        None.

        """
        # setup file paths variable
        DirectoryList = []
        filePaths = []

        # Read all directory, subdirectories and file lists
        dirName = os.getcwd()

        for root, directories, files in os.walk(dirName):
            for directory in directories:
                # Create the full filepath by using os module.
                if key in directory:
                    folderPath = os.path.join(dirName, directory)
                    DirectoryList.append(folderPath)

        # Loop over the identified directories to store the file paths
        for directName in DirectoryList:
            for root, directories, files in os.walk(directName):
                for filename in files:
                    # Create the full filepath by using os module.
                    filePath = os.path.join(root, filename)
                    filePaths.append('.'+filePath.split(dirName)[1])

        # writing files to a zipfile
        if len(filePaths) != 0:
            zip_file = zipfile.ZipFile(dir_name+'.zip', 'w')
            with zip_file:
                # writing each file one by one
                for file in filePaths:
                    zip_file.write(file)

            FilePaths = [path for path in os.listdir('.') if key in path]

            for path in FilePaths:
                shutil.rmtree(path)

            print("\n")
            print(f'{dir_name}.zip file has been created successfully!\n')

        return
