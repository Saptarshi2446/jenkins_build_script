def remote = [:]


node {

      stage('execute') {
                     withCredentials([sshUserPrivateKey(credentialsId: 'new-ubuntu_pem_file', keyFileVariable: 'identity', passphraseVariable: 'pass', usernameVariable: 'ubuntu')]) 
   {
    remote.user = ubuntu
    remote.identityFile = identity
    remote.name = "ubuntu"
    remote.host = "65.0.104.53"
    remote.allowAnyHosts = true
         

    sshCommand remote: remote, command: 'ls'
    sshCommand remote: remote, command: 'sudo pwd'
    sshCommand remote: remote, command: 'sudo rm -rf /home/ubuntu/deployment/agent-install.sh'
    sshCommand remote: remote, command: 'sudo chmod 777 /home/ubuntu/deployment'
    sshPut remote: remote, from: 'agent-install.sh', into: '/home/ubuntu/deployment'
    sshCommand remote: remote, command: 'cd deployment/'
    sshCommand remote: remote, command: 'sudo chmod 777 /home/ubuntu/deployment/agent-install.sh'
    sshCommand remote: remote, command: 'sudo sh /home/ubuntu/deployment/agent-install.sh'
    sshCommand remote: remote, command: 'ls /home/ubuntu/deployment'
    sshCommand remote: remote, command: 'sudo systemctl status zabbix-agent\n\n'
    sshCommand remote: remote, command: 'sudo systemctl status zabbix-agent | grep active'


    }
   }
}
