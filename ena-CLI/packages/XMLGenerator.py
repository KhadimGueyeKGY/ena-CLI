from lxml import etree
import os
import hashlib
import sys
import platform
import shutil
import pandas as pd
from datetime import datetime

class XML_generator:
    
    # ------------------Method to build the submission XML file
    def project_submission_xml(result_directory,args):
        # Create the root element
        try:
            manifestFile = pd.read_excel(args.manifestFile, sheet_name="project")
        except Exception as e:
            print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
            
        submission_set = etree.Element('SUBMISSION_SET')
        submission = etree.SubElement(submission_set, 'SUBMISSION')
        actions = etree.SubElement(submission, 'ACTIONS')
        
        # Create the first ACTION element with ADD
        action1 = etree.SubElement(actions, 'ACTION')
        add1 = etree.SubElement(action1, 'ADD') 
        
        # Create the second ACTION element with HOLD
        head = [i for i in manifestFile]
        for i in range(len(manifestFile[head[0]])):
            if '#' not in manifestFile[head[0]][i]:
                if not pd.isna(manifestFile['date'][i]):
                    action2 = etree.SubElement(actions, 'ACTION')
                    formatted_date = manifestFile['date'][i].strftime('%Y-%m-%d')
                    hold = etree.SubElement(action2, 'HOLD', HoldUntilDate=formatted_date)
    
        # Generate the XML string
        submission_xml = etree.tostring(submission_set, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        
        # Specify the path for the submission XML file
        submission_file = os.path.join(result_directory, 'submission.xml')
    
        # Write to the XML file
        with open(submission_file, 'wb') as f:
            f.write(submission_xml)
    
        print(f"\033[93mSubmission XML file saved to: {submission_file}\033[0m")
        
        # Return the file path
        return submission_file

    #----------------- Method to build project XML file
    def generate_project_xml(result_directory,args):
        try:
            manifestFile = pd.read_excel(args.manifestFile, sheet_name="project")
        except Exception as e:
            print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
        # Create the root element
        project_set = etree.Element('PROJECT_SET')

        head = [i for i in manifestFile]
        for i in range(len(manifestFile[head[0]])):
            if '#' not in manifestFile[head[0]][i]:
                # Create the PROJECT element
                project = etree.SubElement(project_set, 'PROJECT', alias=manifestFile['alias'][i])
                
                # Add the NAME element
                if not pd.isna(manifestFile['name'][i]):
                    name = etree.SubElement(project, 'NAME')
                    name.text = manifestFile['name'][i]
                
                # Add the TITLE element
                title = etree.SubElement(project, 'TITLE')
                title.text = manifestFile['Title'][i]
                
                # Add the DESCRIPTION element
                description = etree.SubElement(project, 'DESCRIPTION')
                description.text = manifestFile['description'][i]
                
                # Add the SUBMISSION_PROJECT element
                submission_project = etree.SubElement(project, 'SUBMISSION_PROJECT')
                sequencing_project = etree.SubElement(submission_project, 'SEQUENCING_PROJECT')
                # Add the Locus_Tag element
                if not pd.isna(manifestFile['LocusTag'][i]) and not args.test:
                    # Add the LOCUS_TAG_PREFIX element
                    locus_tag_prefix = etree.SubElement(sequencing_project, 'LOCUS_TAG_PREFIX')
                    locus_tag_prefix.text = manifestFile['LocusTag'][i]
                elif not pd.isna(manifestFile['LocusTag'][i]) and args.test :
                    print(f"\033[91mError: Registration for Locus Tags is not permitted on the test server . \033[0m")
                
                # Add the PROJECT_LINKS element
                if not pd.isna(manifestFile['PubMed'][i]):
                    project_links = etree.SubElement(project, 'PROJECT_LINKS')
                    project_link = etree.SubElement(project_links, 'PROJECT_LINK')
                    xref_link = etree.SubElement(project_link, 'XREF_LINK')
                    db = etree.SubElement(xref_link, 'DB')
                    db.text = "PUBMED"
                    id_element = etree.SubElement(xref_link, 'ID')
                    id_element.text = manifestFile['PubMed'][i]
                
                # Add the PROJECT_ATTRIBUTE element
                if not pd.isna(manifestFile['Study Attributes Tag'][i]) and not pd.isna(manifestFile['Study Attributes Value'][i]):
                    project_attribute = etree.SubElement(project, 'PROJECT_ATTRIBUTE')
                    tag = etree.SubElement(project_attribute, 'TAG')
                    tag.text = manifestFile['Study Attributes Tag'][i]
                    value = etree.SubElement(project_attribute, 'VALUE')
                    value.text = manifestFile['Study Attributes Value'][i]
            
        # Specify the path for the submission XML file
        submission_file = os.path.join(result_directory, 'project.xml')
    
        # Write the XML to the file
        with open(submission_file, 'wb') as f:
            f.write(etree.tostring(project_set, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    
        print(f"\033[93mProject XML file saved to: {submission_file}\033[0m")
        return submission_file



    # ------------------Method to build the submission XML file
    def build_submission_xml(result_directory):
        # Create XML elements
        submission_set = etree.Element('SUBMISSION')
        actions_elt = etree.SubElement(submission_set, 'ACTIONS')
        action_elt = etree.SubElement(actions_elt, 'ACTION')
        add_elt = etree.SubElement(action_elt, 'ADD')

        # Create XML tree
        submission_xml = etree.ElementTree(submission_set)

        # Specify the path for the submission XML file
        submission_file = os.path.join(result_directory, 'submission.xml')

        # Write to the XML file
        with open(submission_file, 'wb') as f:
            submission_xml.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"\033[93mSubmission XML file has been saved to: {submission_file}\033[0m")
        return submission_file

    def generate_sample_xml(result_directory, args):
        try:
            # Read the manifest file into a pandas DataFrame
            manifest = pd.read_excel(args.manifestFile, sheet_name="sample",header=1)
        except Exception as e:
            print(f"\033[91mError: Failed to read the manifest file {args.manifestFile}.\033[0m\nException: {e}")
            sys.exit() 
            
        # Create the root element of the XML document
        sample_set = etree.Element('SAMPLE_SET')
        
        # Iterate over rows in the manifest DataFrame
        for i in range(len(manifest)):
            # Check if the 'tax_id' value is not NaN
            if not pd.isna(manifest['tax_id'][i]):
                # Ignore lines starting with '#'
                if '#' not in str(manifest['tax_id'][i]) :
                    # Create a new 'SAMPLE' element
                    sample = etree.SubElement(sample_set, 'SAMPLE', alias=str(manifest['sample_alias'][i]))
                    
                    # Add 'TITLE' element to the sample
                    title = etree.SubElement(sample, 'TITLE')
                    title.text = str(manifest['sample_title'][i])
                    
                    # Add 'SAMPLE_NAME' element to the sample
                    sample_name = etree.SubElement(sample, 'SAMPLE_NAME')
                    taxon_id = etree.SubElement(sample_name, 'TAXON_ID')
                    taxon_id.text = str(manifest['tax_id'][i])
                    scientific_name = etree.SubElement(sample_name, 'SCIENTIFIC_NAME')
                    scientific_name.text = str(manifest['scientific_name'][i])
                    
                    # Add 'SAMPLE_ATTRIBUTES' element to the sample
                    sample_attributes = etree.SubElement(sample, 'SAMPLE_ATTRIBUTES')
                    sample_attribute = etree.SubElement(sample_attributes, 'SAMPLE_ATTRIBUTE')
                    tag = etree.SubElement(sample_attribute, 'TAG')
                    tag.text = "ENA-CHECKLIST"
                    value = etree.SubElement(sample_attribute, 'VALUE')

                    manifestFile = pd.read_excel(args.manifestFile, sheet_name="sample")
                    manifestFile_head = [h for h in manifestFile]
                    for e in manifestFile_head:
                        if 'ERC' in e:
                            value.text = e
                                
                    # Add 'SAMPLE_ATTRIBUTE' elements to the sample for each attribute in the manifest
                    head = [h for h in manifest]
                    for j in range(4, len(head)):
                        if not pd.isna(manifest[head[j]][i]):
                            sample_attribute = etree.SubElement(sample_attributes, 'SAMPLE_ATTRIBUTE')
                            tag = etree.SubElement(sample_attribute, 'TAG')
                            tag.text = head[j]
                            value = etree.SubElement(sample_attribute, 'VALUE')
                            if head[j] in ['collection date','receipt date'] :
                                value.text = manifest[head[j]][i].strftime('%Y-%m-%d')
                            else: 
                                value.text = str(manifest[head[j]][i])
                            if head[j] in ['geographic location (latitude)','geographic location (longitude)']:
                                units = etree.SubElement(sample_attribute, 'UNITS')
                                units.text = 'DD'
                            elif head[j] == 'host age':
                                units = etree.SubElement(sample_attribute, 'UNITS')
                                units.text = 'years'
                            
        # Create the XML tree
        sample_xml = etree.ElementTree(sample_set)
        
        # Specify the path for the submission XML file
        sample_file = os.path.join(result_directory, 'sample.xml')
        
        # Write the XML tree to the XML file
        with open(sample_file, 'wb') as f:
            sample_xml.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        
        print(f"\033[93mThe sample XML file has been saved to: {sample_file}\033[0m")
        return sample_file


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
            
    # --------------------Method to generate the set XML file
    def antibiogram_generate_set_xml(result_directory, args):
        # Create ANALYSIS_SET element
        analysis_set = etree.Element('ANALYSIS_SET')

        # Create ANALYSIS element
        analysis = etree.SubElement(analysis_set, 'ANALYSIS', alias=args.alias)

        # Add TITLE and DESCRIPTION elements to ANALYSIS
        title = etree.SubElement(analysis, 'TITLE')
        if args.Title:
            title.text = args.Title
        else:
            title.text = f'Antibiogram for study {args.Study}, sample {args.sample}' 
        if args.description:
            description = etree.SubElement(analysis, 'DESCRIPTION')
            description.text = args.description

        # Add STUDY_REF, SAMPLE_REF, and RUN_REF elements to ANALYSIS
        study_ref = etree.SubElement(analysis, 'STUDY_REF', accession=args.Study)
        sample_ref = etree.SubElement(analysis, 'SAMPLE_REF', accession=args.sample)

        # Add ANALYSIS_TYPE element to ANALYSIS
        analysis_type = etree.SubElement(analysis, 'ANALYSIS_TYPE')
        AMR_ANTIBIOGRAM = etree.SubElement(analysis_type, 'AMR_ANTIBIOGRAM')

        # Add FILES element to ANALYSIS
        files = etree.SubElement(analysis, 'FILES')

        # Add FILE element to FILES
        checksum = XML_generator.calculate_md5(args.filename)
        try:
            shutil.copy(args.filename, result_directory)
            filename = os.path.basename(args.filename)
        except Exception as e: 
            print(f"\033[91mError: Unable to copy the file {args.filename} to {result_directory} \033[0m")
            sys.exit()

        file = etree.SubElement(files, 'FILE', filename=filename, filetype="tab", checksum_method="MD5", checksum=checksum)

        # Create XML tree
        xml_tree = etree.ElementTree(analysis_set)

        # Write XML tree to file
        output_path = os.path.join(result_directory, f'Antibiogram_for_{args.sample}.xml')
        xml_tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"\033[93mSubmission Set XML file has been saved to: {output_path}\033[0m")
        return output_path
