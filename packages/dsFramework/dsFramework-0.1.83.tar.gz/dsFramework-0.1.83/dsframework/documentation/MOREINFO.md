## Additional information {#more_info}

### Creating additional forcer/predictable objects
Generating a new project creates a predictable object and a forcer object, if you need additional ones you can use 
the following dsf-cli commands that will inject it to the pipeline after the existing ones. 

Make sure that you are inside generated project folder: <br />
(cd my-new-project)

<br />
Creating a new forcer (will be automatically injected to pipeline after last existing forcer)

    dsf-cli g forcer my-new-forcer 

<br />
Creating a new predictable (will be automatically injected to pipeline after last existing predictable)

    dsf-cli g predictable my-new-predictable 

### Additional server endpoints
When the server is up it exposes a few endpoints:
    
 * http://localhost:8080/parse - Validates input based on input scheme and executes the pipeline. 
 * http://localhost:8080/predict - Validates input based on input scheme and executes the pipeline. 
 * http://localhost:8080/test - Runs a mock test using Data science portal
 * http://localhost:8080/livenessprobe - server response test - returns "alive": True on success.

### Additional commands
* **dsf-cli create-deploy-files** - deploy files generated automatically when creating new project this is an option to create all non exist deploy files, 

  * if deploy file was deleted by mistake you can recreate it 

  * if dsframework version was update with updated deploy files you can delete deploy files and recreate them

* **dsf-cli create-cloud-eval-files** - cloud eval files this is an option to create all non exist cloud eval files

### list of commands:
Display a list of all cli options:

    dsf-cli 