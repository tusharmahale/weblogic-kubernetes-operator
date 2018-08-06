#=======================================================================================
# This is an example of a WLST offline configuration script. This sample demonstrates
# two methods for creating distributed queues. This sample is based on 
# the Basic WebLogic Server Domain template and extends it using the Avitek Medical 
# Records Sample.
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
# Configure the Administration Server and SSL port.
#=======================================================================================

cd('Servers/AdminServer')
set('ListenAddress','')
set('ListenPort', 7001)

create('AdminServer','SSL')
cd('SSL/AdminServer')
set('Enabled', 'True')
set('ListenPort', 7002)

#=======================================================================================
# Define the password for user weblogic. You must define the password before you 
# can write the domain.
#=======================================================================================

cd('/')
cd('Security/base_domain/User/weblogic')
# Please set password here before using this script, e.g. cmo.setPassword('value')

#=======================================================================================
# Set Options:
# - CreateStartMenu:    Enable creation of Start Menu shortcut.
# - ServerStartMode:    Set mode to development.
# - JavaHome: 		Sets home directory for the JVM used when starting the server.
# - OverwriteDomain:    Overwrites domain, when saving, if one exists.
#=======================================================================================

setOption('CreateStartMenu', 'false')
setOption('ServerStartMode', 'dev')
setOption('JavaHome','@JAVA_HOME')
setOption('OverwriteDomain', 'true')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

writeDomain('/storage/tushar/weblogic12.2.1/user_projects/domains/mymedrec')
closeTemplate()

#=======================================================================================
# Reopen the domain.
#=======================================================================================

readDomain('/storage/tushar/weblogic12.2.1/user_projects/domains/mymedrec')

#=======================================================================================
# Extend the domain to include the Avitek Medical Records Sample Applications
#=======================================================================================

addTemplate('/storage/tushar/weblogic12.2.1/wlserver/common/templates/wls/medrec.jar')

#=======================================================================================
# Create a JMS System resource. 
#=======================================================================================

cd('/')
create('medrec-jms-resource', 'JMSSystemResource')
cd('JMSSystemResource/medrec-jms-resource/JmsResource/NO_NAME_0')

#=======================================================================================
# Method 1: Automatically create a JMS distributed queue.
# Create a JMS Queue before you create a cluster. When you create the cluster, 
# this queue will be promoted automatically to a distributed queue with the same 
# JNDI name.
#=======================================================================================

cd('/')
cd('JMSSystemResource/medrec-jms-resource/JmsResource/NO_NAME_0')
myq1=create('myq1','Queue')
myq1.setJNDIName('myq1_jndi')
myq1.setSubDeploymentName('myq1SubDeployment')
myq2=create('myq2','Queue')
myq2.setJNDIName('myq2_jndi')
myq2.setSubDeploymentName('myq2SubDeployment')

cd('/')
cd('JMSSystemResource/medrec-jms-resource')
create('myq1SubDeployment', 'SubDeployment')
create('myq2SubDeployment', 'SubDeployment')

#=======================================================================================
# Target resources to the servers. 
#=======================================================================================

cd('/')
assign('JMSServer', 'MedRecJMSServer', 'Target', 'AdminServer')
assign('JMSSystemResource.SubDeployment', 'medrec-jms-resource.myq1SubDeployment', 'Target', 'MedRecJMSServer')
assign('JMSSystemResource.SubDeployment', 'medrec-jms-resource.myq2SubDeployment', 'Target', 'MedRecJMSServer')

#=======================================================================================
# Create three Managed Servers and configure them.
#
# Note that in this example you need to set the port to a unique value first. If you set
# the ListenAddress first, the ListenAddress and default ListenPort combination would
# be the same as the Administration Server, and you would receive an error.
#
# Migratable servers, which provide for both automatic and manual migration 
# at the server-level, are created automatically when you create the Managed Servers.
#=======================================================================================

cd('/')
create('MedRec1', 'Server')
cd('Server/MedRec1')
set('ListenPort', 8001) 
set('ListenAddress', '')

cd('/')
create('MedRec2', 'Server')
cd('Server/MedRec2')
set('ListenPort', 8011)
set('ListenAddress', '')

#=======================================================================================
# Create and configure a cluster and assign the Managed Servers to that cluster.
#=======================================================================================

cd('/')
create('MedRecCluster', 'Cluster')
assign('Server', 'MedRec1,MedRec2','Cluster','MedRecCluster')
cd('Cluster/MedRecCluster')
set('MulticastAddress', '237.0.0.101')
set('MulticastPort', 8050)
set('WeblogicPluginEnabled', 'true')


#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

updateDomain()
closeDomain()

#=======================================================================================
# Reopen the domain.
#=======================================================================================

readDomain('/storage/tushar/weblogic12.2.1/user_projects/domains/mymedrec')

#=======================================================================================
# Set ReplaceDuplicates option--keep original configuration elements in the domain.
#=======================================================================================

setOption('ReplaceDuplicates','false')

#=======================================================================================
# Method 2: Manually create a JMS distributed queue, and its queue members.
#=======================================================================================

cd('/JMSSystemResource/medrec-jms-resource/JmsResource/NO_NAME_0')
distQ=create('distQ','DistributedQueue')
distQ.setJNDIName('distQ_jndi')

a = ['1', '2']

for n in a:
    qname = "newQueue_" + "auto_" + n
    cd('/JMSSystemResource/medrec-jms-resource/JmsResource/NO_NAME_0')
    q=create(qname,'Queue')
    q.setJNDIName(qname+'_jndi')
    q.setSubDeploymentName(qname+'_SubDeployment')
    cd('/')
    cd('JMSSystemResource/medrec-jms-resource')
    create(qname+'_SubDeployment', 'SubDeployment')
    assign('JMSSystemResource.SubDeployment', 'medrec-jms-resource.'+qname+'_SubDeployment', 'Target', 'MedRecJMSServer_auto_'+n)
    cd('/JMSSystemResource/medrec-jms-resource/JmsResource/NO_NAME_0/DistributedQueue/distQ')
    dqm=create(qname,'DistributedQueueMember')


#=======================================================================================
# Write and close the domain.
#=======================================================================================

updateDomain()
closeDomain()

#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
