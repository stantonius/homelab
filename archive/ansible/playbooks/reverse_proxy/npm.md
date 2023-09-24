# Node Proxy Manager

I tried with Caddy - just couldn't make it work. Using NPM is such a dream to set up and use.

Despite my best efforts, I couldn't automate everything. Therefore for any new machines in the network where I want a domain name associated, I need to do the following manual tasks.

1. Log into Adguard Home > Filters > DNS Rewrites. Because we are using subdomains to access services, all I needed to do was add a single wildcard route in the AGH DNS Rewrite section: `*.stanton.ooo` -> `192.168.1.xxx` 
2. Log into NPM > Hosts > Proxy Hosts and add the domain and IP address, including port number.

## DNS

I bought the domain for our house with Google Domains. It doesn't have an API service through which we can do DNS challenges. So I created a Cloudflare account and transferred the domain over to them. They became the **DNS provider** for the domain. From what I gather, this means that they are the ones that will register and update your domain to all of the public servers to enable DNS to work on the web.

## SSL

Initially I had tried to 

Followed [this post](https://www.nodinrogers.com/post/2022-03-10-certbot-cloudflare-docker/) on how to 