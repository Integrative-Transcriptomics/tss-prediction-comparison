# TSSplorer - A tool for comparing and visualizing predicted transcription start sites in prokaryotes

## What is a transcription start site (TSS) and what do we need it for?
During prokaryotic transcription an RNA strand is synthesized by the protein complex RNA polymerase from 5' to 3' end.  
In the first main phase of transcription, the initiation, the RNA polymerase complex is assembled at the promotor. After assembly the RNA polymerase escapes the promotor and begins forming a strand of complementary bases to the template DNA. The first base to be incorporated is called the transcription start site (TSS). 

Therefore the TSS is the first transcribed base on the DNA template after the promoter as well as the first base in the transcribed RNA strand.  

Studying the TSS of prokaryotes is interesting for several reasons:

- Promoter recognition: The TSS is located near the promoter region. Identifying the TSS helps recongizing important elements of the promoter region.
- Gene annotation and accurate gene mapping: The TSS is essential for correctly annotating the start of genes. 
- Regulatory mechanisms: Many transcription factors bind near the TSS to either repress or enhance transcription. Identifying the TSS helps in mapping these binding sites and understanding their regulatory roles. The region between the TSS and the start codon, the 5' untranslated region, can play important roles in the regulation of translation. Knowing the TSS helps analyzing this region.

More on the biological backgrounds of transcription in prokaryotes in the [wiki](https://github.com/Integrative-Transcriptomics/tss-prediction-comparison/wiki/Prokaryotic-gene-structure-and-transcription).


## What distinguishes TSSplorer from other TSS prediction tools like TSSpredator?
## How to use TSSplorer?
1. Input the following:
   - The name of your project (on the management site you will find your submission under this name)
   - your .wig-files of the forward and the reverse strand that were derived under the same condition (for example in an environment with 30°C)
   - you can multiple forward and reverse files as technical replicates by selecting more files 
   - you can add more conditions by pressing the + button under the conditions
   - The mastertable of TSSpredator for the comparison
   - The .gff-file for the TSS classification
2. If you're done uploading all files first press the Start Prediction button. If the upload was succesful you get a blue feedback message under the button for confirmation
3. once you get the blue feedback message press the Load Management Page button to look at the results 
4. The results might not be ready at this point. Press the reload button to update the statuses of the uploaded files 
5. Once finished you can download the result and visualize it by pressing the corresponding buttons.

Remember that you're not limited to uploading just one project. Head back to the initial page and upload another project, the management page will show all projects that you have submitted while on the TSSplorer website. 
 
## Workflow
## Languages and tools used in this project
- Visualization: Plotly
- Frontend: 
  - Language: JavaScript
  - Framework: React
- Backend: 
  - Python
## Contact
If you encounter any problems using TSSplorer please feel free to create an issue or contact us via email: 



