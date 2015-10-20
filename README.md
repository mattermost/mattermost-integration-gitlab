# GitLab Integration Service for Mattermost

This integrations service posts [issue](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#issues-events), [comment](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#comment-events) and [merge request](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#merge-request-events) events from a GitLab repository into specific Mattermost channels by formatting output from [GitLab's outgoing webhooks](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/web_hooks/web_hooks.md) to [Mattermost's incoming webhooks](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md).

Mattermost community members are invited to fork this repo to create new integrations. To have your integration referenced on http://www.mattermost.org/webhooks/, please mail info@mattermost.com or tweet to [@MattermostHQ](https://twitter.com/mattermosthq). 

## Requirements

To run this integration you need:

1. A **web server** running **Ubuntu 14.04** and **Python 2.7** or compatible versions. 
2. A **[GitLab account](https://about.gitlab.com/)** with a repository to which you have administrator access
3. A **[Mattermost account](http://www.mattermost.org/)** where [incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks)

Many web server options will work, below we provide instructions for [**Heroku**](README.md#heroku-based-install) and a general [**Linux/Ubuntu**](README.md#linuxubuntu-1404-web-server-install) server.
### Heroku-based Install

To install this project using Heroku, you will need: 

1. A **Heroku account**, available for free at [Heroku.com](https://signup.heroku.com/)
2. A **GitHub account**, available for free at [GitHub.com](https://github.com/join) 

Here's how to start:

1. **Create a copy of this project to manipulate**
  1. Log in to your GitHub account. Go to the [Github repository of this project](https://github.com/mattermost/mattermost-integration-gitlab/edit/it-edits/README.md) and click **Fork** in the top-right corner to create a copy of this project that you control and manipulate.
2. **Deploy your project copy to Heroku**
  1. Go to your [**Heroku Dashboard**](https://dashboard.heroku.com/apps) and click **+** in the top-right corner then **Create New App**. Give your app a unqiue name (like `mattermost-[YOUR_GITHUB_USERNAME]`), select your region and click **Create App**.
  2. Heroku directs you to the **Deploy** tab of the dashboard for your new app, select **GitHub** as your connection option, then click **Connect to GitHub** at the bottom of the screen to authorize Herkou to access your GitHub account.
  3. In the pop up window, click **Authorize Application** to allow Heroku to access your accounts repositories. On your Heroku dashboard, select your account in the first drop-down then search for the repo we created earlier by forking this project. Type `mattermost-integration-gitlab` in the **repo-name** field, then click **Search** and then the **Connect** button once Heroku finds your repository.
  4. Scroll to the bottom of the new page. Under the **Manual Deploy** section, make sure the `master` branch is selected then click **Deploy Branch**. After a few seconds you'll see a confirmation that the app has been deployed.
  5. At the top of your app dashboard, go to the **Settings** tab and scroll down to the **Domains** section. Copy the URL below **Heroku Domain** (we'll refer to this as `http://<your-heroku-domain>/` and we'll need it in the next step)
  6. Leave your Heroku interface open as we'll come back to it to finish the setup.

3. **Connect your project to your GitLab account for outgoing webhooks**
 1. Log in to GitLab account and open the project from which you want to receive updates and to which you have administrator access. From the left side of the project screen, click on **Settings** > **Web Hooks**. In the **URL** field enter `http://<your-heroku-domain>/` from the previous step, plus the word `new_event` to create an entry that reads **`http://<your-heroku-domain>/new_event`** so events from your GitLab project are sent to your Heroku server. Make sure your URL has a leading `http://` or `https://`.
 2. On the same page, under **Trigger** select **Push events**, **Comment events**, **Issue events**, **Merge Request events**
 3. (Recommended but optional): Encrypt your connection from GitLab to your project by selecting **Enable SSL verification**. If this option is not available and you're not familiar with how to set it up, contact your GitLab System Administrator for help.
 3. Click **Add Web Hook** and check that your new webhook entry is added to the **Web hooks** section below the button.
 4. Leave this page open as we'll come back to it to test that everything is working.
 
4. **Set up your Mattermost instance to receive incoming webhooks**
 1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to **Account Settings** > **Integrations** > **Incoming Webhooks**.
 2. Under **Add a new incoming webhook** select the channel in which you want GitLab notifications to appear, then click **Add** to create a new entry.
 3. Copy the contents next to **URL** of the new webhook you just created (we'll refer to this as `https://<your-mattermost-webhook-URL>` and add it to your Heroku server).
 4. Go back to your Heroku app dashboard under the **Settings** tab. Under the **Config Variables** section, click **Reveal Config Vars**
     1. Type `MATTERMOST_WEBHOOK_URL` in the **KEY** field and paste `https://<your-mattermost-webhook-URL>` into the **VALUE** field, then click **Add**.
     2. In the second **KEY** field, type `PUSH_TRIGGER` and in the corresponding **VALUE** field, type `True`.

5. **Test your webhook integration**
  1. If your GitLab project is in active development, return to the **Settings** > **Web Hooks** page of your GitLab project and click **Test Hook** to send a test message about one of your recent updates from your GitLab project to Mattermost. You should see a notification on the Gitlab page that the hook was successfully executed. In Mattermost, go to the channel which you specified when creating the URL for your incoming webhook and make sure that the message delivered successfully.
  2. If your GitLab project is new, try creating a test issue and then verify that the issue is posted to Mattermost.
  3. Back on the settings tab of your Heroku app dashboard, under the **Config Variables**, click **Reveal Config Vars** and then click the `X` next to the **PUSH_TRIGGER** field you added. This config variable was used for testing only, and is better left turned off for production
  4. If you have any issues, please go to http://forum.mattermost.org and let us know which steps in these instructions were unclear or didn't work.


### Linux/Ubuntu 14.04 Web Server Install

The following procedure shows how to install this project on a Linux web server running Ubuntu 14.04. The following instructions work behind a firewall so long as the web server has access to your GitLab and Mattermost instances. 

To install this project using a Linux-based web server, you will need a Linux/Ubuntu 14.04 web server supporting Python 2.7 or a compatible version. Other compatible operating systems and Python versions should also work. 

Here's how to start:

1. **Set up your Mattermost instance to receive incoming webhooks**
 1. Log in to your Mattermost account. Click the three dot menu at the top of the left-hand side and go to **Account Settings** > **Integrations** > **Incoming Webhooks**.
 2. Under **Add a new incoming webhook** select the channel in which you want GitLab notifications to appear, then click **Add** to create a new entry.
 3. Copy the contents next to **URL** of the new webhook you just created (we'll refer to this as `https://<your-mattermost-webhook-URL>`).

2. **Set up this project to run on your web server**
 1. Set up a **Linux Ubuntu 14.04** server either on your own machine or on a hosted service, like AWS.
 2. **SSH** into the machine, or just open your terminal if you're installing locally.
 3. Confirm **Python 2.7** or a compatible version is installed by running:
    - `python --version` If it's not installed you can find it [here](https://www.python.org/downloads/)
 4. Install **pip** and other essentials:
    - `sudo apt-get install python-pip python-dev build-essential`
 5. Clone this GitHub repo:
    - `git clone https://github.com/mattermost/mattermost-integration-gitlab.git`
    - `cd mattermost-integration-gitlab`
 6. Install integration requirements:
    - `sudo pip -r requirements.txt`
 7. Add the following lines to your `~/.bash_profile`:
    - `export MATTERMOST_WEBHOOK_URL=https://<your-mattermost-webhook-URL>` This is the URL you copied in the last section
    - `export PUSH_TRIGGER=True`
    - `export PORT=<your-port-number>` The port number you want the integration to listen on (defaults to 5000)
 8. Source your bash profile:
    - `source ~/.bash_profile`
 9. Run the server:
    - `python server.py`

3. **Connect your project to your GitLab account for outgoing webhooks**
 1. Log in to GitLab account and open the project from which you want to receive updates and to which you have administrator access. From the left side of the project screen, click on **Settings** > **Web Hooks**. In the **URL** field enter `http://<your-web-server-domain>/` from the previous step, plus the word `new_event` to create an entry that reads **`http://<your-web-server-domain>/new_event`** so events from your GitLab project are sent to your Heroku server. Make sure your URL has a leading `http://` or `https://`.
 2. On the same page, under **Trigger** select **Push events**, **Comment events**, **Issue events**, **Merge Request events**
 3. (Recommended but optional): Encrypt your connection from GitLab to your project by selecting **Enable SSL verification**. If this option is not available and you're not familiar with how to set it up, contact your GitLab System Administrator for help.
 4. Click **Add Web Hook** and check that your new webhook entry is added to the **Web hooks** section below the button.
 5. Leave this page open as we'll come back to it to test that everything is working.

4. **Test your webhook integration**
  1. If your GitLab project is in active development, return to the **Settings** > **Web Hooks** page of your GitLab project and click **Test Hook** to send a test message about one of your recent updates from your GitLab project to Mattermost. You should see a notification on the Gitlab page that the hook was successfully executed. In Mattermost, go to the channel which you specified when creating the URL for your incoming webhook and make sure that the message delivered successfully.
  2. If your GitLab project is new, try creating a test issue and then verify that the issue is posted to Mattermost.
  3. Remove the `export PUSH_TRIGGER=True` line from your `~/.bash_profile` and source it again `source ~/.bash_profile`. This was used for testing only, and is better left turned off for production
  4. If you have any issues, please go to http://forum.mattermost.org and let us know which steps in these instructions were unclear or didn't work.
