In order to simplify and make the test set-up easier, I have deployed an instance in google Cloud using the free tier Compute Engine.

In that machine I have installed a postgresql database and an apache2 server and I use the external IP of said machine to make the connections.

# PostgreSQL 
* After installing postgres using ```sudo apt install postgresql``` I had to define a new firewall rule to grant access from all IPs to this VM with the tag 'postgres' using tcp on port 5432
* I then modified the file ```postgresql.conf``` to change ```listen_address = '*'```
* And the file ```pg_hba.conf``` to change the ipV4 and ipV6 (not really neccessary) to ```host all all 0.0.0.0/0 trust``` and ```host all all ::/0 trust```
* Restarted the service using ```sudo systemctl restart postgres```

I now can access the database from my own computer in order to access the information needed for the API.

# Apache2 
* First of all I installed apache2 using ```sudo apt install apache2```
* I created a virtual host for my images by creating a new file in the ```/etc/apache2/sites-available``` directory called ```images.conf``` with the following information:

```
<VirtualHost *:80>
    ServerName [external IP]
    DocumentRoot /var/www/images
    <Directory /var/www/images>
        Options Indexed FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```
* I then enabled the virtual host using ```sudo a2ensite [external IP]```
* And to set the permissions for the image directory and so that the Apache2 server has access to the images I ran the following commands: ```sudo chown -R www-data:www-data /var/www/images``` ```sudo chmod -R 755 /var/www/images```
* After restarting the server using ```sudo systemctl restart apache2``` I had the server working
* In order to get the actual images to store I made a new firewall rule to allow SFPT traffic