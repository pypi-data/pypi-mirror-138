#####
pynad
#####
An application to download, sync, organize and prepare the microdata and metadata of the Brazilian National Household Survey, **Pesquisa Nacional por Amostra de Domicílios Contínua** - **Pnadc** - fielded by the Instituto Brasileiro de Geografia e Estatística, `IBGE <http://www.ibge.gov.br>`_.

The **PNADC** is a rotating panel survey. The residential dwellings sampled for a panel are visited five times, quarterly. Every quarter a new panel starts, thus there are five active panels in visits 1 to 5. However, IBGE only disseminates Pnadc microdata as cross-section datasets, aggregating records from distinct panels. The *trimestral* and the *anual-trimestre* datasets are aggregates of the distinct visits of the five panels surveyed in a quarter; the *anual-visita* datasets are annual aggregates of first or fifth visit interviews, comprised by four panels visited for the first or fifth time in a year.

----------------
What pynad does?
----------------
**IBGE periodically releases new PNADC datasets and documents. Eventually, previously released datasets and documents are patched. Currently, there are more than a hundred files to download and monitor for updates.**

Pynad ascertains one always have the latest versions of data and documents, and helps to keep track of the versions used in an application. It clones the *Microdados* folder of the Pnadc distributions at IBGE's `FTP server <ftp://ftp.ibge.gov.br/>`_ as a local archive, a compressed **zip** file, syncing it at user demand.

**PNADC datasets are disseminated as text files with fixed width records. The position of each variable in the record must be declared to load them. The full metadata (names and columns of variables, categories etc.) are in binary xls Excel files.**

Pynad converts the original microdata to standard **csv** text files, conveniently organizes copies of the original *dicionários de variáveis*, and generates machine and human readable **json** text files containing all metadata. The new files are stored in the archive containing the local copy of the PNADC, in distinct folders.

When the local copy is synced, pynad updates the metadata and **csv** files on a need basis.

**PNADC datasets are organized for use as a quarterly or annual cross-section survey, mixing records from 4 or 5 distinct panels. One panel has variables scattered in different datasets. Though dwellings are identified, households and individuals are not. Population weights are not available for the panels**

Pynad creates another archive for panel files. It separates the panels retrieving their records from the cross-sectional datasets and generates a **csv** microdata file for each panel. Then pynad identifies the households and individuals in each dwelling and generates a **csv** microdata file with the keys for each panel.

Finally, pynad joins the panels and identifiers, and reshapes the joined datasets as identified individual records. Original variables have up to five instances in the identified individual records. E.g. for literacy, v3001, the identified individual record has v3001_1, v3001_2 v3001_3, v3001_4, v3001_5.

After reshaping, it calculates and adds panel population weights to the records. Then the records are split in variable blocks: basic, education, labour, income etc. A **csv** microdata file of identified individual records is created for each block of every panel.

When the local copy is synced, and the metadata and **csv** files updated, pynad updates the panel files on a need basis.

-------
Install
-------
`Windows <https://docs.python.org/3/using/windows.html#install-layout-option>`_ users should add Python to the PATH environment variable.

Use `pip <https://docs.python.org/3/installing/index.html#installing-index>`_ to install pynad.

************
Requirements
************
Four additional packages will be installed: `Tablib <https://pypi.org/project/tablib/>`_, `xlrd <https://pypi.org/project/xlrd/>`_, `xlwt <https://pypi.org/project/xlwt/>`_, `PyQt5 <https://pypi.org/project/PyQt5/>`_.

A computer with **16GB RAM** is recommended, as it can use more than 12GB when processing large panels.

Optionally, pynad's performance will improve if a command line compression utility is available.

***********
Performance
***********
IBGE disseminates microdata in text files with fixed width field records. Pynad does not load the content of the original microdata files as numeric data types. It operates with text records converted to comma separated values. Handling, writing and compressing text files, particularly those with lenghty records, takes time, around 10-20 minutes to process a panel. In the first use, some hours will be required to process the more than 30 panels available.

Archives with compressed files have one major drawback: there is no fast and safe way to delete a compressed file. Compression utilities that offer a delete option actually replace the archive by a new one excluding the "deleted" files. Therefore, it takes more time to delete a small file from a large archive than to delete a large file.

The standard Python package `zipfile <https://docs.python.org/3/library/zipfile.html?highlight=zipfile#module-zipfile>`_ does not have a method to delete files. Although it can be easily implemented - write a temporary archive excluding the undesirable files, exclude the old archive, and rename the temporary archive to replace it - its performance is very bad when compared to that of compression utilities such as `zip <http://infozip.sourceforge.net/Zip.html>`_ or `7zip <https://www.7-zip.org/>`_. In Linux, usually **zip** is already installed or is available in the software repositories, and **7zip** can be installed using the **p7zip-full** package. Windows users must make sure the utilitiy is on the system PATH.

Pynad will try to subprocess **zip** or **7zip** to delete files from the archives. If none is found, pynad will resort to the standard library to remove outdated files from the archives.
