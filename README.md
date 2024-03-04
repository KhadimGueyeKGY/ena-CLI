# ENA-CLI

## Introduction
ENA-CLI is a command-line tool designed to facilitate the validation and submission of data to the European Nucleotide Archive (ENA). This tool streamlines the process of preparing and uploading data files, ensuring they meet ENA's submission requirements.

## Prerequisites
Ensure you have the following dependencies installed:
```
pip install argparse pandas lxml
```

## File Upload Reminder
Before using the ENA-CLI for other submission (5), ensure you have uploaded your files to ENA using the Webin file uploader. Detailed instructions on how to upload files can be found [here](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html#uploading-files-to-ena).

## Usage

### 1. Project Submission

#### Usage
```
python ena-CLI.py project -h
```

#### Example
```
python ena-CLI.py project -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 2. Sample Submission

#### Usage
```
python ena-CLI.py sample -h
```

#### Example
```
python ena-CLI.py sample -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 3. Run Submission

#### Usage
```
python ena-CLI.py run -h
```

#### Example
```
python ena-CLI.py run -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/run -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-C`: Center name of the submitter (optional)
- `-t`: Use Webin test service (optional)

### 4. Genome Assembly Submissions

#### Usage
```
python ena-CLI.py genome -h
```

#### Example
```
python ena-CLI.py genome -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/genome -c genome -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-c`: Assembly submission type (choices: genome, transcriptome)
- `-C`: Center name of the submitter (optional)
- `-t`: Use Webin test service (optional)

### 5. Other Submission

#### Usage
```
python ena-CLI.py other -h
```

#### Example
```
python ena-CLI.py other -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/ -a AMR_ANTIBIOGRAM -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-a`: Analysis type (choices: GENOME_MAP, REFERENCE_ALIGNMENT, SEQUENCE_ANNOTATION, ASSEMBLY_GRAPH, PROCESSED_READ, PATHOGEN_ANALYSIS, AMR_ANTIBIOGRAM, COVID-19_FILTERED_VCF, COVID-19_CONSENSUS, PHYLOGENY_ANALYSIS)
- `-C`: Center name of the submitter (optional)
- `-t`: Use Webin test service (optional)

## Options Explanation

### Mandatory Options
- `-u`: Webin submission account: Indicates the Webin submission account.
- `-p`: Password: Indicates the password for the Webin submission account.
- `-m`: Manifest file: Specifies the path to the manifest file.
- `-a`: Analysis type: Specifies the type of analysis provided in the XML.
- `-c`: Assembly submission type: Specifies the type of assembly submission.

### Optional Options
- `-C`: Center name: Specifies the center name of the submitter.
- `-t`: Test submission: Submits the data as a test (optional).

## Contact Information
For any errors or assistance, please contact the [ENA helpdesk](https://www.ebi.ac.uk/ena/browser/support).
