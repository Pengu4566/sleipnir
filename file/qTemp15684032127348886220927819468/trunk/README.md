QueueTemplate
===========
Version 2019.2.0

This template is to be used for all scripts that consumes orchestrator queues. Its aim is to be a minimal and enforce best practices in a non-invasive manner.

## 1. Features



### Exception Screenshots

On every application exceptions that occurs in a section that normally involves UI interactions an exception screenshot is taken and saved to disc. If there is a risk that these screenshots could contain sensitive data, it can easily be disabled.

The folder in which to save these screenshots is set from the config. If the path provided in the config is not rooted (absolute) it is rejected by the framework which will overwrite this value to a system temp folder.

### Standard reporting

If enabled, a standard report is created and saved to disc. The standard report contains basic information about every transaction. It should be used if this information cannot easily be made available to relevant parties in some other way. By default, the transaction information logged in this way contains the following:

| TransactionID     | Status                                | Type | Timestamp                           |
| ----------------- | ------------------------------------- | ---- | ----------------------------------- |
| TransactionNumber | Success/Error/Business Rule Exception |      | Now.ToString("yyyy-MM-dd HH:mm:ss") |



In the same manner as for exception screenshots a rooted target folder is enforced. This feature can be disabled by setting the target path as empty in the configuration, which is the default.

### Exception handling

In the case of a system exception, the robot first tries to exit all applicable applications gracefully. If this fails, the robot will terminate the application processes.

### Retries

The number of retries for a transaction is set as a property on the target orchestrator queue. However, there is also a value for this in the configuration that should match this server value. The reason is that some actions need to be taken only in the case where the maximum retries have been reached.

It is also possible to enable retries on initialization errors, which is disabled by default.

### Environment diagnostics

To make it easier to debug a process that is showing instability, one can enable environment diagnostics at a certain "transaction frequency". If enabled, the robot will check the running computers RAM and CPU usage. It will also check the RAM and CPU used by the target processes.  

### Standardized logging

Whenever a log is sent by a framework routine it will be prefixed with [FRAMEWORK]. This is in order to separate framework logs from those written by the developer.

### Alerts

Certain transactions are of such importance that they cannot be allowed to fail without notification. The framework can optionally send an alert with the severity level **Error** if a transaction fails with a system exception. This can be useful in a service context. Keep in mind that this will put pressure on support maintenance. Use with caution.



## 2. Basic usage

### Implementation

The framework consist of 3 placeholder routines that need to be populated by the developer. They are the following:

#### 1. InitAllApplications

Open all relevant applications here. This routine is also responsible for setting the application state to the state required as preconditions by the process routine.

Always remember to check that the preconditions for the process are met when this routine has run, otherwise one runs the risk of burning transaction data when the preconditions are not met.

#### 2.CloseAllApplications

Close all relevant applications. Surround all specific application closer routines by try catch blocks. This is so that the robot tries to close all applications gracefully before terminating the processes.

#### 3.Process

Does the main work of the script. The preconditions must be the same as the postconditions here.

### Configuration

All configuration values that determine the operation of the framework is set in the "Framework" sheet of the configuration file. Script/Process specific configuration values should be defined in the "Settings" sheet.

Most framework configuration values have sensible defaults and need not be altered. Some configurations value are, however, process specific and needs to be set by the developer. These are:

| Name                     | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| SourceQueue              | The Queue from which the robot retrieves its transactions    |
| logF_BusinessProcessName | The name of the process that the script is a part of.        |
| logF_ScriptName          | Friendly name of the script.                                 |
| applicationProcessNames  | Not strictly mandatory to set, but should always be considered carefully. It is a comma seperated list of all application process names that is to be killed if a graceful closing routine fails. |



Some other important configuration values:

| Name                            | Type | Description                                                  | Default           |
| ------------------------------- | ---- | ------------------------------------------------------------ | ----------------- |
| MaxiumTransactionsProcess       | Int  | Optionally sets a limit on how many transactions may be processed in one job. If 0, no limit is set. | 0                 |
| MaxRetryNumber                  | Int  | The number of times to retry a transaction that failed with a system exception. This should match the number set in the orchestrator source queue. | 0                 |
| MaxErrorsInSequence             | Int  | Sets a threshold on how many times transactions can fail in sequence before the script is terminated. If 0, no such limit is set. | 0                 |
| MaxInitRetryNumber              | Int  | The number of times to retry after a system exception in the initialization step. | 0                 |
| SystemDiagnosticsFrequency      | Int  | The frequency of environment diagnostics. If 0, no diagnostics is run. | 0                 |
| AlertOnTransactionError         | Bool | If true, an alert with severity error is raised if a transaction fails with a system exception. | False             |
| AlertOnTransactionError_Message | Str  | The alert message.                                           | Transaction Error |
| DisableScreenshots              | Bool | If True, no screenshots are taken by the framework           | False             |
| ProjectPath_temp                | Str  | Project path for storing temporary files. If none is set, a default path under system folder temp will be set |                   |
| ProjectPath_static              | Str  | Project path for storing files that need to be kept. If none is set, a default path under system folder temp will be set |                   |
| StandardReportPath              | Str  | Path to folder in which to store standard reports. If none is set, standard reporting is disabled. If set, but not rooted, a default folder will be set instead. |                   |
| StandardReportDateFormat        | Str  | The date format with which to name standard report files.    |                   |
| ExScreenshotsFolderPath         | Str  | Project path for exception screenshots. If none is set or if the path is not rooted, a default path under system folder temp will be set |                   |
|                                 |      |                                                              |                   |

### Script arguments.

Certain framework configurations overwritten with package arguments. If they are not explicitly set, they default to the configuration value. They are the following:

| Name                                | Type | Overwrites                   |
| ----------------------------------- | ---- | ---------------------------- |
| in_int_delayBeforeUIActions         | Int  | DelayBeforeUIActions         |
| in_int_MaximumTransactionsProcessed | Int  | MaximumTransactionsProcessed |
| in_int_MaxErrorsInSequence          | Int  | MaxErrorsInSequence          |
| in_int_SystemDiagnosticsFrequency   | Int  | SystemDiagnosticsFrequency   |





## Best practices



The following is a short version on how to apply best practices when working with the template. A full version of the best practices of UiPath development can be found at https://newinnovationmanagement.sharepoint.com/:w:/s/NewInnovationManagement/EWiA1X02ychBvkECqyv8qfIB0ZWje1gZQa6bAfNx72__QQ?e=Sb2SZq. 



### Keep it clean.

Try to keep the code as clean as possible. Try to sort all scripts into appropriate folders so that files can be easily found and their usage inferred. Remember to name all activities in order to simplify debugging. In the annotations of the "Process" script, make sure to very clearly state the pre/post conditions.

### Workflow arguments.

Try, as far as possible, to keep the argument structure of the framework files.

### Making changes.

When modifying a framework to better suit your needs, make sure to always make these changes explicit.

### Documentation.



### Making suggestions.

If you have ideas that you think could improve the framework, please send your suggestions to johan.sjogren@new-innovation.com.	



## Change log.











##### 

​		

​				



