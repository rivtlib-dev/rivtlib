
rivtbook Folders
--------------------------------------------------------------------------------

    [rivtbk-]Book-Label/             rivtbook report folder              
        ├── .help/                        help files
        ├── .vscode/                      optional VSCode settings   
        ├── README.txt                    rivt-generated book as text
        ├── [rivtbook-report]-1.py        rivtbook generating script                  
        ├── [_rivtbk-public]/             public subset of rivt files         
            ├── [rvbk-101-]folder name    rivtbook folder
            ├── [rvbk-102-]folder name    rivtbook folder        
            ├── [rvbk-201-]folder name    rivtbook folder         
                ...
        ├── [_rstdocs]/                   rivt-generated rst files
            ├── _downloads/                    
            ├── _static/                                                       
            ├── rv101-filename1.rst            
            ├── rv102-filename2.rst                          
            ├── rv201-filename3.rst          
                ...
        ├── [_pdfdocs]/                   pdf docs and rivtbook report
            ├── pdf auxiliary folders     
            ├── report-title.pdf
            ├── rv101-filename1.pdf             
            ├── rv102-filename1.pdf             
            ├── rv201-filename3.pdf
        └── [_rv_stor]/                    rivt-generated source files
            ├── [logs]/                          log files
                ├── rv101-log.txt
                └── rv102-log.txt
            ├── [sect]/                          sections not printed                    
                ├── rv202-5d.txt  
                ├── rv103-4t.txt                         
                └── rv301-2r.txt               
            ├── [temp]/                          temp files
                └── rv101-label3.tex
            ├── [vals]/                          values files
                ├── v101-2.csv
                └── v102-3.csv         
            └── output.dat 
        ├── [bk1-]folder name              rivtbook chapter folder
            ├── [rv001-]filename1.py          rivt file       
            ├── [downloads]/                    files to download      
                └── conc-vals.txt 
            ├── [img]/                          page layout images              
                ├── favicon.png    
                ├── covlogo1.png    
                ├── runlogo1.png
                └── fig1.png
            ├── [data]/                          tables    
                └── steel-vals.csv                                                 
            ├── [vals]/                          values files
                ├── v101-2.csv
                └── v102-3.csv         
            └── tools/                           OS shell commands               
                └── opensees.sh                           
        ├── [bk2-]folder name             rivtbook chapter folder
                ...        
        └── [bk3-]folder name             rivtbook chapter folder
                ...
