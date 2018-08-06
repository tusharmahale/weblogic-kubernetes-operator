#=======================================================================================
# This is an example of a WLST offline configuration script. This example uses the 
# Basic WebLogic Server Domain template to create an domain that creates specific
# resources similar to those used in the Avitek MedRec sample. This example does not
# recreate the MedRec example in its entirety, nor does it deploy any sample applications.
#
# This sample uses Derby Database that is installed with your product.
# Before starting the Administration Server, you should start Derby Database
# by issuing one of the following commands:
#
# Windows: WL_HOME/common/derby/bin/startNetworkServer.cmd
# UNIX: WL_HOME/common/derby/bin/startNetworkServer.sh
#
# (WL_HOME refers to the top-level installation directory for WebLogic Server.)
#
# Please note that many values used in this script are subject to change based 
# on your WebLogic installation and the template you are using.
#
# Usage: 
#      java weblogic.WLST <WLST_script> 
#
# Where: 
#      <WLST_script> specifies the full path to the WLST script.
#=======================================================================================

#=======================================================================================
# Open a domain template. Assumes WebLogic Platform installed at /storage/tushar/weblogic12.2.1/wlserver.
# Update pathname as appropriate.
#=======================================================================================

readTemplate('/storage/tushar/weblogic12.2.1/wlserver/common/templates/wls/wls.jar')

#=======================================================================================
# Configure the Administration Server and the SSL port.
#=======================================================================================

cd('Servers/AdminServer')
set('Name', 'MedRecServer')
set('ListenAddress','')
set('ListenPort',7001)
set('TunnelingEnabled', 1)

create('MedRecServer','SSL')
cd('SSL/MedRecServer')
set('Enabled', 'True')
set('ListenPort', 7002)

#=======================================================================================
# Define the password for user weblogic.
#=======================================================================================

cd('/')
cd('Security/base_domain/User/weblogic')
# Please set password here before using this script, e.g. cmo.setPassword('value')

#=======================================================================================
# Create JDBC Data Sources and set the database and driver properties.
#=======================================================================================

# Creating a Data Source
cd('/')
jdbcSR = create("MedRecGlobalDataSource","JDBCSystemResource")
cd('JDBCSystemResource/MedRecGlobalDataSource/JdbcResource/MedRecGlobalDataSource')
connectionPoolParams = create('connectionPoolParams', 'JDBCConnectionPoolParams')
connectionPoolParams.setInitialCapacity(1)
connectionPoolParams.setMaxCapacity(10)
connectionPoolParams.setCapacityIncrement(1)
connectionPoolParams.setShrinkFrequencySeconds(900)
connectionPoolParams.setTestConnectionsOnReserve(1)
connectionPoolParams.setTestTableName("SYSTABLES")
driverParams = create('driverParams', 'JDBCDriverParams')
driverParams.setDriverName("org.apache.derby.jdbc.ClientDriver")
driverParams.setUrl("jdbc:derby://localhost:1527/demo;create=true")
driverParams.setPasswordEncrypted("PBPUBLIC")
cd('JDBCDriverParams/NO_NAME_0')
create('medrec','Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
cmo.setValue('PBPUBLIC')
cd('/JDBCSystemResource/MedRecGlobalDataSource/JdbcResource/MedRecGlobalDataSource')
dsParams = create('dataSourceParams', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', ['jndi/MedRecGlobalDataSource'])

# Creating a Transactional Data Source
cd('/')
jdbcXASR = create("MedRecGlobalDataSourceXA","JDBCSystemResource")
cd('JDBCSystemResource/MedRecGlobalDataSourceXA/JdbcResource/MedRecGlobalDataSourceXA')
connectionPoolParams = create('connectionPoolParams', 'JDBCConnectionPoolParams')
connectionPoolParams.setInitialCapacity(2)
connectionPoolParams.setMaxCapacity(10)
connectionPoolParams.setCapacityIncrement(1)
connectionPoolParams.setShrinkFrequencySeconds(900)
connectionPoolParams.setTestConnectionsOnReserve(1)
connectionPoolParams.setTestTableName("SYSTABLES")
driverParams = create('driverParams', 'JDBCDriverParams')
driverParams.setDriverName("org.apache.derby.jdbc.ClientXADataSource")
driverParams.setUrl("jdbc:derby://localhost:1527/demo;create=true")
driverParams.setPasswordEncrypted("PBPUBLIC")
cd('JDBCDriverParams/NO_NAME_0')
create('medrec','Properties')
cd('Properties/NO_NAME_0')
create('user', 'Property')
cd('Property/user')
cmo.setValue('PBPUBLIC')
cd('../..')
create('DatabaseName', 'Property')
cd('Property/DatabaseName')
cmo.setValue('demo')
cd('../../../../../..')
dsXAParams = create('dataSourceParams', 'JDBCDataSourceParams')
cd('JDBCDataSourceParams/NO_NAME_0')
set('JNDIName', ['jndi/MedRecGlobalDataSourceXA'])

#=======================================================================================
# Create a JMS System resource. 
#=======================================================================================

cd('/')
create('MedRec-jms', 'JMSSystemResource')
cd('JMSSystemResource/MedRec-jms/JmsResource/NO_NAME_0')

#=======================================================================================
# Create the JMS Connection Factory and its subdeployment
#=======================================================================================

connectionFactory = create('MedRecQueueFactory', 'ConnectionFactory')
cd('ConnectionFactory/MedRecQueueFactory')
set('JNDIName', 'jms/MedRecQueueConnectionFactory')
set('SubDeploymentName', 'MedRecQueueFactorySubDeployment')

cd('/')
cd('JmsSystemResource/MedRec-jms')
create('MedRecQueueFactorySubDeployment', 'SubDeployment')

#=======================================================================================
# Create a JMS JDBC Store. The JMS JDBC Store is used to persist JMS messages to ensure 
# they are not lost if a problem occurs before they are processed. 
#=======================================================================================

cd('/')
myJDBCStore = create('MedRecJMSJDBCStore', 'JdbcStore')
myJDBCStore.setPrefixName('MedRec')
myJDBCStore.setDataSource(jdbcSR)

#=======================================================================================
# Create the JMS Server. 
#=======================================================================================

cd('/')
myJMSServer = create('MedRecJMSServer', 'JMSServer')
myJMSServer.setPersistentStore(myJDBCStore)

#=======================================================================================
# Create the JMS Queues and their subdeployments.
#=======================================================================================

cd('/')
cd('JMSSystemResource/MedRec-jms/JmsResource/NO_NAME_0')
reqQueue = create('RegistrationQueue','Queue')
reqQueue.setJNDIName('jms/REGISTRATION_MDB_QUEUE')
reqQueue.setSubDeploymentName('RegistrationQueueSubDeployment')
mailQueue = create('MailQueue','Queue')
mailQueue.setJNDIName('jms/MAIL_MDB_QUEUE')
mailQueue.setSubDeploymentName('MailQueueSubDeployment')

cd('/')
cd('JMSSystemResource/MedRec-jms')
create('RegistrationQueueSubDeployment', 'SubDeployment')
create('MailQueueSubDeployment', 'SubDeployment')

#=======================================================================================
# Create an e-mail session to add e-mail capabilities. 
#=======================================================================================

cd('/')
mailSession = create('MedicalRecordsMailSession', 'MailSession')
mailSession.setJNDIName('mail/MedRecMailSession')
cd('MailSession/MedicalRecordsMailSession')
set('Properties','mail.user=joe,mail.host=mail.mycompany.com')

#=======================================================================================
# Target resources to the servers. 
#=======================================================================================

cd('/')
assign('JDBCSystemResource', 'MedRecGlobalDataSource', 'Target', 'MedRecServer')
assign('JDBCSystemResource', 'MedRecGlobalDataSourceXA', 'Target', 'MedRecServer')
assign('JMSSystemResource', 'MedRec-jms', 'Target', 'MedRecServer')
assign('JdbcStore', 'MedRecJMSJDBCStore', 'Server', 'MedRecServer')
assign('JMSServer', 'MedRecJMSServer', 'Target', 'MedRecServer')
assign('MailSession', 'MedicalRecordsMailSession', 'Target', 'MedRecServer')
assign('JMSSystemResource.SubDeployment', 'MedRec-jms.RegistrationQueueSubDeployment', 'Target', 'MedRecJMSServer')
assign('JMSSystemResource.SubDeployment', 'MedRec-jms.MailQueueSubDeployment', 'Target', 'MedRecJMSServer')

#=======================================================================================
# Write the domain and close the domain template.
# Update the path parameter of writeDomain as appropriate.
#=======================================================================================

setOption('OverwriteDomain', 'true')
writeDomain('@MW_HOME/user_projects/domains/sampleMedRecDomain')
closeTemplate()

print 'The script returns successfully!'
#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
