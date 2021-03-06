#AIKIF
#####Artificial Intelligence Knowledge Information Framework (PRE-Alpha)

This is an information classification framework that maps structured or freeform data to 
a standard knowledge store.<br />

Raw data is collected via Agents and the Mapper uses your business rules to convert and 
store the information in a machine usable format (by linking to ontologies).<br />

Your AI software can link to AIKIF by setting up logging watch-points to define success / 
failure along with the range of input parameters. Goals and plans are defined by breaking 
them down to smaller tasks until the task can be run by a tool in the Toolbox.<br />

A tool is any python wrapped function or application and is easily extensible.<br />


###Progress
Area | status
 --- | --- |
| Code base version            | Pre-Alpha    |
| Public package version | 0.1.2        |
| Date notes updated     | 12th-May-2015   |

###Core Data
Data type | description |
 --- | ---                
| events     | any time or date based subset of information gets logged here  |
| facts      | the text of the information |
| contacts   | person/website details extracted and linked from text or column in table |
| locations  | physical location in world, or virtual location on network / computer disk |
| processes  | actions that occur - logged events and planned jobs  |
| projects   | an AIKIF project, when used with toolbox methods can be automated   |
 
 

###Key Programs
|Filename | description |
 --- | ---      
|go_web_aikif.bat | starts the web server for the AIKIF admin interface|
|AI_CLI.py		  | Command Line interface to add and query data|
|agents/*.py      | agents to collect and aggregate raw data |
|environments/*.py | defined environments for agents to run in |
|toolbox/*.py     | toolbox methods used to perform a specific task |
|dataTools/*.py   | various programs for managing data flow |
|lib/*.py         | commonly used functions (NOTE - these may move) |
|core_data.py     | classes to manage the core data types |
|knowledge.py     | processs raw data to information |
|index.py		  | creates text indexes of all the files|
|search.py		  | searches, using both indexes and ontologies|
|mapper.py        | applies business rules to map raw input to aikif data structures|
|context.py       | determines user context|
|bias.py          | user defined ranking of raw data by source / type / person / date|

##Quick Start
This github repository [https://github.com/acutesoftware/AIKIF](https://github.com/acutesoftware/AIKIF) contains the latest code, but the current public release is available via

`pip install aikif`

To start the web interface use `aikif/web_app/web_aikif.py` or the batch file `aikif\go_web_aikif`
 
![screenshot of web interface](https://github.com/acutesoftware/AIKIF/blob/master/doc/web-if-v02.jpg "Screenshot of web interface") 
 
####Simple Usage
In its simplest form AIKIF can be used to manage your projects and tasks, by updating information from scripts and tracking via the web application
```
my_biz = project.Project(name='Acute Software', type='business', desc='Custom Software')
my_biz.add_detail('website', 'http://www.acutesoftware.com.au')
my_biz.add_detail('email', 'djmurray@acutesoftware.com.au')
```

####Logging data
You can use AIKIF as a database to manage adhoc data logging tasks
```
proj2 = project.Project(name='Sales Log', desc='Record list of sales')
proj2.add_detail('Note', 'List of sales taken from manual entries in test program')

tbl_exp = cls_datatable.DataTable('expenses.csv', col_names=['date', 'amount', 'details'])
proj2.record(tbl_exp, 'Expense', ['2015-02-13', 49.94, 'restaurant'])
proj2.record(tbl_exp, 'Expense', ['2015-02-15', 29.00, 'petrol'])
proj2.record(tbl_exp, 'Expense', ['2015-02-17', 89.95, 'fringe tickets'])
```

####Data Collection Usage

```
p = aikif.project.Project('update Country reference', type='Auto')
p.add_task(1, 'download file', aikif.toolbox.web_download)
p.add_task(2, 'extract zip', aikif.toolbox.zip_util)  # not implemented
p.add_task(3, 'overwrite TXT to database staging', aikif.toolbox.data_load) 

p.add_param(task=1, url='http://www.')
p.add_param(task=1, dest_zip = 'T:\data\download\country')
p.add_param(task=3, tbl='S_REF_COUNTRY')
p.execute()
```
This will execute the methods for each task using the specified parameters to update the table from the web


####Map information
Define how columns in raw data should be mapped
```
m = aikif.mapper('custom mapper for countries', tbl = 'S_REF_COUNTRY')
m.add_col('code', data_type='STR', map_to_col='COUNTRY_CODE')
m.add_col('Name', data_type='STR', map_to_col='COUNTRY_NAME')
m.add_col('Continent', data_type='STR', map_to_col='CONTINENT')
m.add_col('Population', data_type='NUMBER', map_to_col='POPULATION')
```


####Define your own Toolbox methods
Say you have a program 'my_average.py' which calculates averages that you want to include in the toolbox methods
```
t = aikif.toolbox.Toolbox()
t.add_tool(1, 'Calc Average', src=T:\dev\src\python\my_tools\my_average.py')

p2 = aikif.project.Project('Aggregate Country by Continent')
p2.add_task(1, 'Fetch source data', aikif.toolbox.data_view)
p2.add_task(2, 'Aggregate Population', t['Calc Average'])

p2.add_param(task=1, tbl = 'S_REF_COUNTRY' )
p2.add_param(task=2, group_by_col = 'CONTINENT', measure_col='POPULATION' )

p2.execute()  # with no parameters, data outputs to console
```

###More Information
[Requirements Documentation](https://github.com/acutesoftware/AIKIF/blob/master/doc/AIKIF_requirements.rst)<br />
[Design Notes](https://github.com/acutesoftware/AIKIF/blob/master/doc/AIKIF_design.rst)<br />
[Overview Diagram](https://github.com/acutesoftware/AIKIF/blob/master/doc/AIKIF-Overview.jpg)<br />

