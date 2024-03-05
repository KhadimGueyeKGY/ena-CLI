import pandas as pd
import sys , os
from lxml import etree
import hashlib

class XMLGenerator:
    # -----------------------Calculation of the MD5 hash for a given file
    def calculate_md5(filename_full):
        try:
            # Open the file in binary read mode and read its contents
            with open(filename_full, 'rb') as file:
                file_contents = file.read()
            
            # Calculate the MD5 hash of the file's contents
            file_md5 = hashlib.md5(file_contents).hexdigest()
            
            return file_md5
        
        except Exception as e:
            print(f"\033[91mError: Unable to calculate MD5 hash for file {filename_full}\033[0m")
            print("Exception:", e)
            sys.exit()
    
    @staticmethod
    def other_submission(result_directory, args):
        try:
            manifestFile = pd.read_excel(args.manifestFile, sheet_name="Other Analyses", header = 1)
        except Exception as e:
            print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
        
        # Create ANALYSIS_SET element
        analysis_set = etree.Element('ANALYSIS_SET')
        head = [i for i in manifestFile]
        for i in range(len(manifestFile[head[0]])):
            if '#' not in manifestFile[head[0]][i]:
                # Create ANALYSIS element
                analysis = etree.SubElement(analysis_set, 'ANALYSIS', alias=manifestFile['alias'][i])
        
                # Add TITLE and DESCRIPTION elements to ANALYSIS
                if not pd.isna(manifestFile['TITLE'][i]):
                    title = etree.SubElement(analysis, 'TITLE')
                    title.text = manifestFile['TITLE'][i]
            
                if not pd.isna(manifestFile['DESCRIPTION'][i]):
                    description = etree.SubElement(analysis, 'DESCRIPTION')
                    description.text = manifestFile['DESCRIPTION'][i]
        
                # Add STUDY_REF, SAMPLE_REF, and RUN_REF elements to ANALYSIS
                study_ref = etree.SubElement(analysis, 'STUDY_REF', accession=manifestFile['STUDY_REF'][i])
                sample_ref = etree.SubElement(analysis, 'SAMPLE_REF', accession=manifestFile['SAMPLE_REF'][i])

                
                if not pd.isna(manifestFile['RUN_REF'][i]):
                    run_ref = etree.SubElement(analysis, 'RUN_REF', accession=manifestFile['RUN_REF'][i])
        
                # Add ANALYSIS_TYPE element to ANALYSIS
                analysis_type = etree.SubElement(analysis, 'ANALYSIS_TYPE')
                if args.analysisType == 'GENOME_MAP':
                    GENOME_MAP = etree.SubElement(analysis_type, 'GENOME_MAP')
                    PROGRAM = etree.SubElement(GENOME_MAP, 'PROGRAM')
                    PROGRAM.text = manifestFile['PROGRAM'][i]
                    PLATFORM = etree.SubElement(GENOME_MAP, 'PLATFORM')
                    PLATFORM.text = manifestFile['PLATFORM'][i]
                elif args.analysisType == 'REFERENCE_ALIGNMENT':
                    REFERENCE_ALIGNMENT = etree.SubElement(analysis_type, 'REFERENCE_ALIGNMENT')
                    ASSEMBLY = etree.SubElement(REFERENCE_ALIGNMENT, 'ASSEMBLY')
                    STANDARD = etree.SubElement(ASSEMBLY, 'STANDARD' ,accession = manifestFile['ASSEMBLY'][i])
                    SEQUENCE = etree.SubElement(REFERENCE_ALIGNMENT, 'SEQUENCE' , accession = manifestFile['SEQUENCE'][i])
                else:
                    analysis_type_set = etree.SubElement(analysis_type, args.analysisType)
                
        
                # Add FILES element to ANALYSIS
                files = etree.SubElement(analysis, 'FILES')
        
                # Add FILE element to FILES
                file_path = os.path.join(args.inputDir, manifestFile['FILES'][i] )
                checksum = XMLGenerator.calculate_md5(file_path)
                
        
                file = etree.SubElement(files, 'FILE', filename=manifestFile['FILES'][i], filetype=manifestFile['filetype'][i], checksum_method="MD5", checksum=checksum)
        
                # Create XML tree
                xml_tree = etree.ElementTree(analysis_set)
        
                # Write XML tree to file
        output_path = os.path.join(args.inputDir, f'other_submission.xml')
        xml_tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        
        print(f"\033[93mSubmission Set XML file has been saved to: {output_path}\033[0m")

        return output_path
        
