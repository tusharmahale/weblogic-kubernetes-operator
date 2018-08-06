#=======================================================================================
# This is an example of a WLST offline configuration script. This example demonstrates
# how to create a single-cluster domain. This sample is based on the Basic WebLogic 
# Server Domain template and extends it using the Avitek Medical Records Sample 
# extension template.
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
# Open a domain template. 
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

writeDomain('/storage/tushar/weblogic12.2.1/user_projects/domains/medrecCluster')
closeTemplate()

#=======================================================================================
# Reopen the domain.
#=======================================================================================

readDomain('/storage/tushar/weblogic12.2.1/user_projects/domains/medrecCluster')

#=======================================================================================
# Extend the domain to include the Avitek Medical Records Sample Applications
#=======================================================================================

addTemplate('/storage/tushar/weblogic12.2.1/wlserver/common/templates/wls/medrec.jar')

#=======================================================================================
# Create three Managed Servers and configure them.
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

cd('/')
create('MedRec3', 'Server')
cd('Server/MedRec3')
set('ListenPort', 8021)
set('ListenAddress', '')


#=======================================================================================
# Create and configure a cluster and assign the Managed Servers to that cluster.
#=======================================================================================

cd('/')
create('MedRecCluster', 'Cluster')
assign('Server', 'MedRec1,MedRec2,MedRec3','Cluster','MedRecCluster')
cd('Cluster/MedRecCluster')
set('MulticastAddress', '237.0.0.101')
set('MulticastPort', 8050)
set('WeblogicPluginEnabled', 'true')

#=======================================================================================
# Create a new application deployment. Uncomment the code to add your application 
# deployment information.
#
# Note that all application deployments that were defined before the cluster is
# created are automatically targeted to the cluster once the cluster is created. 
# For example, the MedRecEar and PhysicianEAR deployments are defined in the Avitek 
# Medical Records Sample extension template. These applications are automatically target 
# to the cluster when it is created.
#=======================================================================================

#cd('/')
#myApp=create('myAppDeployment', 'AppDeployment')
#myApp.setSourcePath('/storage/tushar/weblogic12.2.1/user_projects/applications/myApp')
#assign('AppDeployment', 'myAppDeployment', 'Target', 'MedRecCluster')

#=======================================================================================
# Write the domain and close the domain template.
#=======================================================================================

updateDomain()
closeDomain()

#=======================================================================================
# Exit WLST.
#=======================================================================================

exit()
