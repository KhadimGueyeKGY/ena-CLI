import pandas as pd
import os , sys
import subprocess

class webin:

    def webin_submission(manifest, args, webin_cli, sample, type):
        # Build the command based on the provided arguments
        command = [
            f"java -jar {webin_cli}",
            f"-context {type}",
            f"-manifest '{manifest}'",
            f"-inputDir {args.inputDir}",
            f"-userName {args.username}",
            f"-password {args.password}"
        ]
    
        # Add optional arguments if provided
        if args.test:
            command.append("-test")
        if args.centerName:
            command.append(f"-centerName '{args.centerName}'")
    
        # Execute the command - validation
        try:
            subprocess.run(" ".join(command+['-validate']), shell=True, check=True)
            print(f"\033[93m\nValidation successful. {sample}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91m\nValidation error. {sample}\033[0m\nException: {e}")
            sys.exit()

        # Execute the command - submission
        try:
            subprocess.run(" ".join(command+['-submit']), shell=True, check=True)
            print(f"\033[93m\nSubmission successful. {sample}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91m\nSubmission error. {sample}\033[0m\nException: {e}")
            sys.exit()
        
    def run_submission(result_directory,args, webin_cli):
        try:
            manifestFile = pd.read_csv (args.manifestFile, sep='\t', header = 1)
        except Exception as e:
            print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
        head = [i for i in manifestFile]
        for i in range(len(manifestFile['sample'])):
            if not pd.isna(manifestFile['sample'][i]):
                manifest = os.path.join(result_directory, f"manifest_run_{manifestFile['sample'][i]}.txt")
                with open(manifest , 'w') as file:
                    for j in range(len(head)) : 
                        if not pd.isna(manifestFile[head[j]][i]):
                            if 'file_name' in head[j]:
                                #file_name = os.path.join('../',args.inputDir,manifestFile[head[j]][i])
                                file_name = manifestFile[head[j]][i]
                                file.write(f"FASTQ\t{file_name}\n")
                            else:
                                file.write(f'{head[j].upper()}\t{manifestFile[head[j]][i]}\n')

            webin.webin_submission(manifest , args, webin_cli, manifestFile['sample'][i], args.context)

    
    def genome_submission(result_directory,args, webin_cli):
        try:
            manifestFile = pd.read_csv (args.manifestFile, sep='\t')
        except Exception as e:
            print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
        head = [i for i in manifestFile]
        for i in range(len(manifestFile['SAMPLE'])):
            if not pd.isna(manifestFile['SAMPLE'][i]):
                manifest = os.path.join(result_directory, f"manifest_genome_{manifestFile['SAMPLE'][i]}.txt")
                with open(manifest , 'w') as file:
                    for j in range(len(head)) : 
                        if not pd.isna(manifestFile[head[j]][i]):
                            file.write(f'{head[j].upper()}\t{manifestFile[head[j]][i]}\n')

            webin.webin_submission(manifest , args, webin_cli, manifestFile['SAMPLE'][i], 'genome')
            
        