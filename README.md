# About
LazyRedTeamer is a collection of my own tools that I use to automate setting up infrastructure, recon, explotiations and post-exploitation. 

# install
`git pull <repo>`

`export PATH="<path to the repo>/LazyRedTeamer/bin:$PATH"`

check by running `lazytest` it runs `whoami`, so you should see your username

# Tools

### nscan
Runs a very aggresive nmap scan command for you. Just do nscan <ip>/<ip range>/<list of ips> and it will do an aggresive nmap scan. Very good for certs/CTFs and labs.

### nxcrecon
Runs `nxc` command on most protocols. Specify the username(s) and password(s) (either single or a file) and the <ip>/<ip range>/<list of ips> and it will do the rest for you. You can also spesifcy --no-bruteforce, --continue-on-sucess and --local-auth if you need those flags to be added behind every protocol that they apply to.

### adrecon
Runs bloodhound-python and uses impacket to dump all kerberoastable and asp-rep roastable accounts. Greate for certs/CTFs and labs. Also works on companies that does not monitor their AD logs. 
g
