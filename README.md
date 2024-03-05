# ENA-CLI

## Introduction
ENA-CLI is a command-line tool designed to facilitate the validation and submission of data to the European Nucleotide Archive (ENA). This tool streamlines the process of preparing and uploading data files, ensuring they meet ENA's submission requirements.

## Prerequisites
Ensure you have the following dependencies installed:
```
pip install argparse pandas lxml
```

## File Upload Reminder
Before using the ENA-CLI for submission, ensure you have uploaded your files to ENA using the Webin file uploader. Detailed instructions on how to upload files can be found [here](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html#uploading-files-to-ena).

## Usage

### 1. Project Submission

#### Usage
```
python ena-CLI project -h
```

#### Example
```
python ena-CLI project -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 2. Sample Submission

#### Usage
```
python ena-CLI sample -h
```

#### Example
```
python ena-CLI sample -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 3. Run Submission

#### Usage
```
python ena-CLI run -h
```

#### Example
```
python ena-CLI run -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/run -t
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
python ena-CLI genome -h
```

#### Example
```
python ena-CLI genome -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/genome -c genome -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-c`: Assembly submission type (choices: genome, transcriptome)
- `-C`: Center name of the submitter (optional)
- `-t`: Use Webin test service (optional)

## Targeted Command

The `targeted` command facilitates the submission of targeted sequences to the public repository ENA (European Nucleotide Archive). It requires the following mandatory arguments:

- `-u`, `--username`: Webin submission account (e.g., Webin-XXX).
- `-p`, `--password`: Password for the submission account.
- `-m`, `--manifestFile`: Path to the manifest file specifying the details of the submission. The manifest file should follow the template provided in `templates/templates.xlsx`.
- `-i`, `--inputDir`: Path to the input directory containing the files declared in the manifest file.

Additionally, the following optional arguments can be provided:
- `-C`, `--centerName`: The center name of the submitter (mandatory for broker accounts).
- `-t`, `--test`: Use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived.

### Usage Example:

```
python ena-CLI targeted -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/targeted -t
```


### 5. Other Submission

#### Usage
```
python ena-CLI other -h
```

#### Example
```
python ena-CLI other -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/other -a AMR_ANTIBIOGRAM -t
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