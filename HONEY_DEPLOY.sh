#!/bin/bash
launch()
{
 echo "
██╗  ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ ████████╗
██║  ██║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝██╔══██╗██╔═══██╗╚══██╔══╝
███████║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝ ██████╔╝██║   ██║   ██║   
██╔══██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝  ██╔═══╝ ██║   ██║   ██║   
██║  ██║╚██████╔╝██║ ╚████║███████╗   ██║   ██║     ╚██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝      ╚═════╝    ╚═╝   
                                                                      


 "
 
{
  
  python fake_ssh.py & 
  python rank.py & 
 } &> /dev/null


}

activity()
{

 echo "ACTIVATING ANALYSIS SYSTEM"
 while true 
 do
    read -p "VIEW ACTIVITY ON HONEYPOT (yes/no):" inp1


    if [[ "$inp1" == "yes"  ]]; then
     {
      python dynamic_graph.py &
     } &> /dev/null
    else
        {
         ps -ef | grep dynamic_graph.py | grep -v grep | awk '{print $2}' | xargs kill 
         ps -ef | grep rank.py | grep -v grep | awk '{print $2}' | xargs kill
        } &> /dev/null 
     break
    fi
 done
}

deactivate()
{
while true 
do
   read -p "DEACTIVATE HONEYPOT (yes/no):" inp2


   if [[ "$inp2" == "yes"  ]]; then
   {
    { 
     ps -ef | grep fake_ssh.py | grep -v grep | awk '{print $2}' | xargs kill 
     break
    } &> /dev/null
   }
   else
    read -p "Do you want to swith to ACTVITY ANALYSIS (yes/no)" inp3
    if [[ "$inp3" == "yes" ]] ; then
     activity
    else
     deactivate
    fi
   fi
done
}



echo "LAUNCHING FAKE SSH SERVER"
launch

activity

deactivate







