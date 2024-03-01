import argparse
import os , sys
import pandas as pd

from packages.XMLGenerator import XML_generator
from packages.submission import submission
from packages.antibiogram import validation
from packages.webin import webin

# color https://gist.github.com/Prakasaka/219fe5695beeb4d6311583e79933a009

# run 
# https://github.com/enasequence/webin-cli/releases/latest 
webin_cli = 'packages/webin-cli-7.0.1.jar'


def get_args(): # https://docs.python.org/3/library/argparse.html
    epilog = ("""
            \033[93mNote:
            (1) \033[0mPlease register your project and sample object before registering the antibiogram. 
            Here is the link for more information: \033[94mhttps://ena-docs.readthedocs.io/en/latest/\033[0m.
            \033[93m(2) \033[0mPlease make sure to provide the title and description using single quotes if they contain spaces or special characters. 
            For any error or assistance please contact the ENA helpdesk: \033[94mhttps://www.ebi.ac.uk/ena/browser/support \033[0m
        """) 
    parser = argparse.ArgumentParser(description='Script for validating AMR antibiograms and optionally submitting them to the public repository ENA.'
                                     ,epilog=epilog)
    
    # Create subparsers
    subparsers = parser.add_subparsers(title='\033[93mSubcommands\033[0m', dest='subcommand')
    
    # 1. Project submission
    project = subparsers.add_parser('project', help='Register a Study (Project)',epilog=epilog)
    
    #### Required arguments
    mandatory_p = project.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_p.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_p.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_p.add_argument('-a', '--alias', type=str, help='Project alias', required=True)
    mandatory_p.add_argument('-D', '--Date', type=str, help='Release data (e.g., 2025-01-12 )', required=True)
    mandatory_p.add_argument('-d', '--description', type=str, help='Detailed study abstract. Use single quotes to provide the description, e.g., \'My Description\'', required=True)
    mandatory_p.add_argument('-T', '--Title', type=str, help='Short description study title. Use single quotes to provide the title, e.g., \'My Title\'', required=True)

    ##### Optional arguments
    optional_p = project.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_p.add_argument('-n', '--name', type=str, default='', help='Study name (Optional)', required=False)
    optional_p.add_argument('-L', '--LocusTag', type=str, help='Locus Tag Prefix Registration (Optional)', required=False)
    optional_p.add_argument('-P', '--PubMed', type=str, help='PubMed Citations Registration (Optional)', required=False)
    optional_p.add_argument('-St', '--StudyAttributesTag', type=str, help='Study Attributes Tag Registration (Optional)', required=False)
    optional_p.add_argument('-Sv', '--StudyAttributesValue', type=str, help='Study Attributes Value Registration (Optional)', required=False)
    optional_p.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    # 2. Sample submission
    sample = subparsers.add_parser('sample', help='Register samples',epilog=epilog)
    #### Required arguments
    mandatory_s = sample.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_s.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_s.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_s.add_argument('-m', '--manifestFile', type=str, help='Sample manifest file (template on: \033[94mhttps://www.ebi.ac.uk/ena/browser/checklist\033[0m)', required=True)

    #### Optional arguments
    optional_s = sample.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_s.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    # 3. run submission
    run = subparsers.add_parser('run', help='Register run',epilog=epilog)
    #### Required arguments
    mandatory_r = run.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_r.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_r.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_r.add_argument('-m', '--manifestFile', type=str, help='run manifest file (template: packages/run_template.txt - tab file)', required=True)
    mandatory_r.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)
    

    #### Optional arguments
    optional_r = run.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_r.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_r.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    # 4. Genome Assemblies 
    Genome = subparsers.add_parser('genome', help='Submitting Genome Assemblies of Individuals or Cultured Isolates - Metagenome Assemblies - Environmental Single-Cell Amplified Genomes - Transcriptome Assemblies - Metatranscriptome Assemblies',epilog=epilog)
    #### Required arguments
    mandatory_g = Genome.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_g.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_g.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_g.add_argument('-m', '--manifestFile', type=str, help='run manifest file (template: packages/run_template.txt - tab file)', required=True)
    mandatory_g.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)
    mandatory_g.add_argument('-c', '--context', choices=['genome','transcriptome'], help=' the assembly submission type', required=True)
    

    #### Optional arguments
    optional_g = Genome.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_g.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_g.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    # 5. Submit Targeted Sequences
    Targeted = subparsers.add_parser('targeted', help='Submit Targeted Sequences',epilog=epilog)
    
    #### Required arguments
    mandatory_t = Targeted.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_t.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_t.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_t.add_argument('-m', '--manifestFile', type=str, help='run manifest file (template: packages/run_template.txt - tab file)', required=True)
    

    #### Optional arguments
    optional_t = Targeted.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_t.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_t.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    
    # 6. antibiograms submission
    antibiograms = subparsers.add_parser('antibiogram', help='Register an Antibiogram',epilog=epilog)
    
    #### Required arguments
    mandatory = antibiograms.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory.add_argument('-f', '--filename', type=str, help='Name of the AMR antibiogram file', required=True)
    mandatory.add_argument('-S', '--Study', type=str, help='Study ID (e.g., PRJEBXXX) to add the antibiograms', required=True)
    mandatory.add_argument('-s', '--sample', type=str, help='Sample ID (e.g., ERSXXXX) to add the antibiograms', required=True)
    mandatory.add_argument('-a', '--alias', type=str, help='Analysis alias to add the antibiograms', required=True)

    #### Optional arguments
    optional = antibiograms.add_argument_group('\033[93mOptional arguments\033[0m')
    optional.add_argument('-T', '--Title', type=str, help='Title of the submission (Optional). Use single quotes to provide the title, e.g., \'My Title\'')
    optional.add_argument('-d', '--description', type=str, help='Description of the submission (Optional). Use single quotes to provide the description, e.g., \'My Description\'')
    optional.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    
    #args = parser.parse_args()
    # Add version argument
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    return parser


def process():
    if len(sys.argv) <= 1: 
        print(get_args().print_help())
        sys.exit()
    args = get_args().parse_args()

    result_directory = 'results'  
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    if args.subcommand == 'project':
        submission_file = XML_generator.project_submission_xml(result_directory,args)
        submission_set_file = XML_generator.generate_project_xml (result_directory, args)
        submission.submit_to_ENA(submission_file , submission_set_file, args, 'PROJECT')

    elif args.subcommand == 'sample':
        submission_file = XML_generator.build_submission_xml(result_directory)
        submission_set_file = XML_generator.generate_sample_xml(result_directory,args)
        submission.submit_to_ENA(submission_file , submission_set_file, args , 'SAMPLE')

    elif args.subcommand == 'run':
        webin.run_submission(result_directory, args  , webin_cli)

    elif args.subcommand == 'genome':
        webin.genome_submission(result_directory, args  , webin_cli)

    elif args.subcommand == 'targeted':
        webin.targeted_submission(result_directory, args  , webin_cli)
        
    elif args.subcommand == 'antibiogram':
        try:
            antibiogram_file = pd.read_csv (args.filename, sep='\t')
        except Exception as e:
            print(f"\033[91mError: reading file {args.filename}.\033[0m\nException: {e}")
            sys.exit() 
        
        validation.validate_biosample_id(antibiogram_file['bioSample_ID'])
        validation.validate_antibiotic_name (antibiogram_file['antibiotic_name'])
        validation.validate_ast_standard(antibiogram_file['ast_standard'])
        validation.validate_resistance_phenotype(antibiogram_file['resistance_phenotype'])
    
        submission_file = XML_generator.build_submission_xml(result_directory)
        submission_set_file = XML_generator.antibiogram_generate_set_xml (result_directory, args)
        submission.submit_to_ENA(submission_file , submission_set_file, args , 'ANALYSIS')

    print(f"\033[93m\n\n-------[ done ]-------\033[0m")
    print(f"\033[94mFor any error or assistance please contact the ENA helpdesk: https://www.ebi.ac.uk/ena/browser/support \n\n\033[0m")


if __name__ == '__main__':
    process()
    