def remote = [:]
remote.name = "ubuntu"
remote.host = "65.0.104.53"
remote.allowAnyHosts = true

node {

      stage('execute') {
                     withCredentials([sshUserPrivateKey(credentialsId: 'new-ubuntu_pem_file', keyFileVariable: 'identity', passphraseVariable: 'pass', usernameVariable: 'ubuntu')]) 
   {
    remote.user = ubuntu
    remote.identityFile = identity

    sshCommand remote: remote, command: 'ls'
    sshCommand remote: remote, command: 'sudo pwd'
    sshCommand remote: remote, command: 'sudo rm -rf agent-install.sh'
    sshCommand remote: remote, command: 'sudo chmod 777 /home/ubuntu/deployment'
    sshPut remote: remote, from: 'agent-install.sh', into: '/home/ubuntu/deployment'
    sshCommand remote: remote, command: 'sudo cd deployment/'
    sshCommand remote: remote, command: 'sudo sh agent-install.sh'
    sshCommand remote: remote, command: 'ls /home/ubuntu/deployment'


    }
   }
}
