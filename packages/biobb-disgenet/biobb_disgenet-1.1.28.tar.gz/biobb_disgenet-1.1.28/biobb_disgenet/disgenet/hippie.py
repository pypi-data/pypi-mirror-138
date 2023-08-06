#!/usr/bin/env python3

"""Module containing the BioBBs DisGeNET class and the command line interface."""
import argparse
import shutil
import pandas as pd
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_disgenet.disgenet.common import *


# 1. Rename class as required
class HIPPIE_disgenet(BiobbObject):
    """
    | biobb_disgenet for retrieving formatted HIPPIE network
    | This class is for donwloading and formatting the second input necessary for the Tool run, which is the formatted HIPPIE network for Homo Sapiens.
    | Wrapper for the HIPPIE Network Database for downloading available collections of genes and variants associated data to Homo Sapiens in a PPI Network.

    Args:
        
        output_file_path (str): Path to the output file, in CSV format.
        
    Examples:
        This is a use example of how to use the building block from Python:

            from biobb_disgenet.disgenet.hippie_disgenet import hippie_disgenet

            hippie_disgenet(
                    output_file_path='hippie_network1')
    Info:

        retrieve_by can be: 
            gene, uniprot, source, evidences

    """

    # 2. Adapt input and output file paths as required. Include all files, even optional ones
    def __init__(self, output_file_path,
                properties = None, **kwargs) -> None:
        properties = properties or {}

        # 2.0 Call parent class constructor
        super().__init__(properties)

        # 2.1 Modify to match constructor parameters
        # Input/Output files
        self.io_dict = { 
            'out': { 'output_file_path': output_file_path } 
        }

        self.format= properties.get("format", "csv")
        # 3. Include all relevant properties here as 
        # self.property_name = properties.get('property_name', property_default_value)

        # Properties specific for BB

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`GDA_disgenet <disgenet.GDA_disgenet.GDA_disgenet>` object."""
        
        # 4. Setup Biobb
        if self.check_restart(): return 0
        self.stage_files()
        
        #self.check_data_params(self.out_log, self.err_log)

        #Check if the output path exists and mandatory params are there
        #output_path = check_output_path(self.io_dict["out"]["output_file_path"], False, "output", self.format, self.out_log, self.__class__.__name__)
        if self.io_dict["out"]["output_file_path"]:
            output_path = check_output_path(self.io_dict["out"]["output_file_path"], False, "output", self.format, self.out_log, self.__class__.__name__)
            print (output_path)
            parse_hippie(output_path, save_out=True, out_log=self.out_log, global_log=self.global_log)
        else:
            raise SystemExit("Fundamental argument is missing, check the input parameter.")
        
        return 0

def hippie_disgenet(output_file_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`Template <template.template.Template>` class and
    execute the :meth:`launch() <template.template.Template.launch>` method."""

    return HIPPIE_disgenet(
                    output_file_path=output_file_path, 
                    properties=properties, **kwargs).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='This class is a wrapper for an associations call of teh DisGeNET database REST API.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    #parser.add_argument('--config', required=False, help='Configuration file')
    # 10. Include specific args of each building block following the examples. They should match step 2
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-output_file_path', required=True, help='Description for the output file path. Accepted formats: json, csv or html.')
    #required_args.add_argument('-password',  required=True)
    args = parser.parse_args()
    args.config = args.config or "{}"
    #properties = settings.ConfReader(config=args.config).get_prop_dic()

    # 11. Adapt to match Class constructor (step 2)
    # Specific call of each building block
    hippie_disgenet(
             output_file_path=output_file_path,
             properties=properties)

if __name__ == '__main__':
    main()

# 12. Complete documentation string


