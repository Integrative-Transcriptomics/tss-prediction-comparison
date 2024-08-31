# TSSplorer - A tool for comparing and visualizing predicted transcription start sites in prokaryotes

## What is a transcription start site (TSS) and what do we need it for?
During prokaryotic transcription an RNA strand is synthesized by the protein complex RNA polymerase from 5' to 3' end.  
In the first main phase of transcription, the initiation, the RNA polymerase complex is assembled at the promotor. After assembly the RNA polymerase escapes the promotor and begins forming a strand of complementary bases to the template DNA. The first base to be incorporated is called the transcription start site (TSS). 

Therefore the TSS is the first transcribed base on the DNA template after the promoter as well as the first base in the transcribed RNA strand.  

Studying the TSS of prokaryotes is interesting for several reasons:

- Identification of new genes and non-coding RNAs: TSS identification in intergenic regions can lead to discovery of new genes and non-coding RNAs
- Applications in biotechnology and medicine: TSSs are crucial for developing targeted gene editing techniques such as CRISPR/Cas
- Promoter recognition: The TSS is located near the promoter region. Identifying the TSS helps recongizing important elements of the promoter region.
- Regulatory mechanisms: Many transcription factors bind near the TSS to either repress or enhance transcription. Identifying the TSS helps in mapping these binding sites and understanding their regulatory roles. The region between the TSS and the start codon, the 5' untranslated region, can play important roles in the regulation of translation. Knowing the TSS helps analyzing this region.

More on the biological backgrounds of transcription in prokaryotes in the [wiki](https://github.com/Integrative-Transcriptomics/tss-prediction-comparison/wiki/Prokaryotic-gene-structure-and-transcription).


## What distinguishes TSSplorer from other TSS prediction tools especially TSSpredator?
Unlike TSSpredator TSSplorer only uses non-enriched data. This means that TSSplorer deals with background noise that arises from data without certain highlighted features, patterns, or subsets of interest.

## How to install and run TSSplorer?
Currently TSSplorer is not being hosted externally and therefore not accessible online.   

To use TSSplorer through a local host do the following:  
Set up the frontend and backend servers as described in the [wiki](https://github.com/Integrative-Transcriptomics/tss-prediction-comparison/wiki/How-to-set-up-the-server-on-your-device).  
After a successful setup of the backend and frontend the full server can be launched using yarn by navigating to your project directory and running `yarn start`.
 
## How to use TSSplorer?
1. Input the following:
   - The name of your project (on the management site you will find your submission under this name)
   - your .wig-files of the forward and the reverse strand that were derived under the same condition (for example in an environment with 30°C)
   - you can submit multiple forward and reverse files as technical replicates by selecting more files. Keep in mind that the number of forward files must match the number of reverse files
   - you can add more conditions by pressing the + button under the conditions
   - The mastertable of TSSpredator for the comparison
   - The .gff-file for the TSS classification  

    Note: Selecting multiple files for the upload on your system
    - Windows:
       - Shift + Click: Click the first file, hold down the Shift key, then click the last file. All files between the first and last will be selected.
       - Ctrl + Click: Hold down the Ctrl key, then click on each file you want to select individually.   
    - macOS: 
      - Shift + Click: Click the first file, hold down the Shift key, then click the last file to select a continuous range of files.
      - Command (⌘) + Click: Hold down the Command (⌘) key, then click on each file you want to select individually.
    - Linux: 
      - Shift + Click: Click the first file, hold down the Shift key, then click the last file to select a range of files.
      - Ctrl + Click: Hold down the Ctrl key, then click on each file you want to select individually.
1. If you're done uploading all files first press the Start Prediction button. If the upload was succesful you get a blue feedback message under the button for confirmation
2. once you get the blue feedback message press the Load Management Page button to look at the results 
3. The results might not be ready at this point. Press the reload button to update the statuses of the uploaded files 
4. Once finished you can download the result and visualize it by pressing the corresponding buttons.

Remember that you're not limited to uploading just one project. Head back to the initial page and upload another project, the management page will show all projects that you have submitted while on the TSSplorer website. 
 
## Workflow

With given Input:

- Conditions with forward and reverse files, Master-Table and GFF-file
 
a prediction of possible TSS together with a confidence value are computed for each condition.  
TSS of forward and reverse files of a condition are predicted seperately but joined in the end.

1. technical replicates are merged together (f.e. multiple multiple forward files)
2. TSS are predicted using a Random Forets Classifier based on "scikit learn"
3. Classification of TSS is done with the GFF-file (classes are f.e. primary or secondary TSS)
4. finding Common TSS of our predicted TSS and TSS of MasterTable (TSS of the MasterTable are the TSS of TSSpredator)
5. common TSS of prediction for forward files and reverse files are joined and visualized in front end

## Languages and tools used in this project
- Visualization: 
  - Upset plots
  - Echarts library
- Frontend: 
  - Language: JavaScript
  - Framework: React
- Backend: 
  - Language: Python
  - Framework: Flask
- TSS Prediction:
  - Scikit-learn
## Contact
If you encounter any problems using TSSplorer please feel free to create an issue or contact us via email: 

markus.henkel@student.uni-tuebingen.de, julian.borbeck@student.uni-tuebingen.de 



