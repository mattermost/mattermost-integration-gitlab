# GitLab to Mattermost Integration

This software creates a process to post [issue](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#issues-events), [comment](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#comment-events) and [merge request](http://doc.gitlab.com/ee/web_hooks/web_hooks.html#merge-request-events) events from a GitLab repository into specific Mattermost channels by formatting output from [GitLab's outgoing webhooks](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/web_hooks/web_hooks.md) to [Mattermost's incoming webhooks](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md).

Mattermost community members are invited to fork this repo to create new integrations. To have your integration referenced on http://www.mattermost.org/webhooks/, please mail info@mattermost.com or tweet to [@MattermostHQ](https://twitter.com/mattermosthq). 

## Requirements

To run this integration you need:

1. A web server supporting Python 2.6 or higher to run this software
2. A [GitLab](https://about.gitlab.com/) account with a repository to which you have administrator access
3. A [Mattermost](http://www.mattermost.org/) account [where incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks)

Regarding 1. there are many options for web servers you can use, below we provide instructions for both **Heroku** and a general **Linux/Ubuntu** server to get something running:  

### Quick Install with Heroku

To install this project using Heroku, you will need: 

1. A Heroku account, available for free from [Heroku.com](http://heroku.com)
2. A GitHub account, available for free from [GitHub.com](http://github.com) 

Here's how to start: 

1. Fork this project using your GitHub account by clicking **Fork** in the top-right corner. 
  2. This creates a copy for you to control and update as you like. 
2. Deploy this project to Heroku
  1. Go to your [**Heroku Dashboard**](https://dashboard.heroku.com/apps) and click **+** in the top-right corner then **New App**. Give your app a name (like "Mattermost GitLab Integration"), select your region and click **Create App**.
  2. On the **Deploy** screen, select **GitHub** at the top, then click **Connect to GitHub** to authorize Herkou to access your GitHub account.
  3. Select your account and type `gitlab-mattermost` into the **repo-name** field, then click **Search** then the **Connect** button next to your repository.
  4. Scroll to the bottom of the new page and under the **Manual Deploy** section click **Deploy Branch**, making sure the `master` branch is selected.
  5. Go to **Domains** > **Settings** and copy **Heroku Domain**.

2. Set up your GitLab outgoing webhook
 1. Log in to your GitLab account, and go to the project you want events pushed from.
 2. From your project page, click _Settings_ in the bottom-left and then click _Web Hooks_. Note that you need have admin access to the project.
 3. In the _URL_ field, enter the following `http://<your-heroku-domain>/new_event`. Make sure to replace `<your-heroku-domain>` with the domain you copied in the last step of the previous install section.
 4. Select all the _Triggers_ you want to be posted into Mattermost, then click _Add Web Hook_.

3. Set up your Mattermost incoming webhook
 1. Log in to your Mattermost account, and open your _Account Settings_ by clicking in the top-left.
 2. Go to the _Integrations_ tab and click _Edit_ next to _Manage your incoming webhooks_.
 3. Select the channel you want the GitLab events to post to, then click _Add_.
 4. Copy the _URL_ from the newly created webhook.
 5. Back on your Heroku app page, go to the _Settings_ tab.
 6. Under the _Config Variables_ section, click the _Reveal Config Vars_ button.
 7. Enter `MATTERMOST_WEBHOOK_URL` for the _KEY_ and paste the URL you copied as the _VALUE_, then click _Add_.

That's it! The integration should now be up and running on Heroku. It might take a minute for the Heroku process to finish starting but after that try performing an action on your GitLab project to trigger a post in Mattermost.

### Manual Install

You of course don't have to use Heroku if you don't want to, you can easily set up the integration to run on practically any web server. It can even go behind your firewall as long as the integration still has access to your GitLab and Mattermost instances.

Below are the loose instructions for setting up the integration on a Linux/Ubuntu server.

3. Set up your Mattermost incoming webhook
 1. Log in to your Mattermost account, and open your _Account Settings_ by clicking in the top-left.
 2. Go to the _Integrations_ tab and click _Edit_ next to _Manage your incoming webhooks_.
 3. Select the channel you want the GitLab events to post to, then click _Add_.
 4. Copy the _URL_ from the newly created webhook and keep it handy for the next steps.

1. Set up your server
 1. Stand-up a Linux/Ubuntu server on AWS, your own machine or somewhere else.
 1. SSH into the machine, or just open your terminal if you're installing locally.
 1. Make sure you have Python 2.7+ installed. If it's not installed you can find it [here](https://www.python.org/downloads/)
    - `python --version`
 2. Install pip and other essentials
    - `sudo apt-get install python-pip python-dev build-essential`
 3. Clone the repo with
    - `git clone https://github.com/mattermost/gitlab-mattermost.git`
    - `cd gitlab-mattermost`
 3. Install integration requirements
    - `sudo pip -r requirements.txt`
 4. Add the following lines to your `~/.bash_profile`
    - `export MATTERMOST_WEBHOOK_URL=<your-webhook-url>` This is the URL you copied in the last section
    - `export PORT=<your-port-number>` The port number you want the integration to listen on (defaults to 5000)
 5. Source your bash profile
    - `source ~/.bash_profile`
 5. Run the server
    - `python server.py`

2. Set up your GitLab outgoing webhook
 1. Log in to your GitLab account, and go to the project you want events pushed from.
 2. From your project page, click _Settings_ in the bottom-left and then click _Web Hooks_.
 3. In the _URL_ field, enter the following `<your-public-server-domain>/new_event`. Make sure to replace `<your-public-server-domain>` with the domain that translates to your public server IP address. Don't forget to include the port if needed. For example, `http://myserver.com:5000/new_event`
 4. Select all the _Triggers_ you want to be posted into Mattermost, then click _Add Web Hook_.

That's it! The integration should now be running and ready to push GitLab events into Mattermost.
