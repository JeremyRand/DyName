DyName
======

VECLabs DyName: Namecoin Dynamic DNS Client  
Copyright 2013 Jeremy Rand AKA biolizard89 of Viral Electron Chaos Laboratories  
https://veclabs.wordpress.com/

Instructions

1. Register a dd/ (domain data) name with namecoind (d/ names are insecure in most cases).
2. Create a shell script which echoes the current IP (examples are provided).
3. Fill in the .conf file which is provided.
4. Execute "./DyName.py ./DyNameConfig.conf" to update your domain, where "./DyNameConfig.conf" is your config file.
5. Assuming it worked, you may wish to schedule DyName.py to run periodically (cron, etc.).

FAQ:

Q: How do I make DyName update an IPv6 domain?  
A: Change the "Resolver" setting in the config file from "ip" to "ip6".  Obviously, your IP-echoing shell script will have to retrieve an IPv6 address also.

Q: Will DyName automatically renew domains that haven't changed IP address?  
A: Set the "RenewBlocks" setting in the config file to the number of remaining blocks left when your domain will be renewed.  Be sure to leave enough time for you to manually renew with namecoind in case something prevents DyName from reaching namecoind... losing control of your domain would be a Bad Thing.

Q: Can I update multiple domains?  
A: Yes, just make more sections in the config file.  However, you can only use one namecoind instance.  Note that this feature is not extensively tested; test reports welcome.

Q: Does it run on Windows?  
A: If you can write a .bat script which gives you an IP, I assume it would probably work.  Test reports welcome.

Q: DyName says "name_update failed for name."  Everything still seems to be working.  What's going on?  
A: If DyName runs more than once per Namecoin block, successful name_update operations won't be visible to DyName until the next block, so it tries again the next time it runs, and fails because namecoind only allows 1 name_update operation per name per block.  This is harmless.

Q: DyName says "I will not allow the name to be stolen without authorization."  What's going on?  
A: Don't use d/ names.  Only use dd/ names with DyName.

Q: How do I make a .bit resolver understand dd/ names?  
A: Use the "import" field from your d/ name, and point it to your dd/ name.

Q: Do all .bit resolvers support the "import" field?  
A: No, and the ones which don't are inherently insecure.  Tell the developer of your favorite .bit resolver to support the "import" field.

Q: Why not use d/ names with DyName?  
A: Because the credentials to update or transfer your d/ name would be on an Internet-connected machine (possibly a front-facing server) with an unencrypted wallet.  If an attacker compromises your server, they could permanently steal your domain.  If you use a dd/ name with DyName, you can always change the "import" field in your d/ name in the event of attack and restore access to yourself.

Q: I don't care if my domain is stolen, I want to use a d/ name with DyName.  
A: Use the "--i-want-my-domain-to-be-stolen" command line flag.  But this is almost always a seriously bad idea.  Really.  Don't do it.

Q: You're awesome.  Can I donate?  
A: I know it, man.  Donations can be made at 15PqJcCUZ2EHxwDm8TegUPYuj6wPtAKPgN (Bitcoin) or NAPEAJkpGjMf4LiDfQx3mNJbjrrp5xw6tn (Namecoin).
