# GitLab to Mattermost Integration

This integration posts events from GitLab to Mattermost by translating output from [GitLab's outgoing webhooks](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/doc/web_hooks/web_hooks.md) to [Mattermost's incoming webhooks](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md).

## Installing

This integration can be run from any web server that supports Python. The simplest way to get it up and running fast is to use Heroku.

**Note: These installation instructions assume you have both a GitLab account with a project you have admin access to, and a Mattermost account where [incoming webhooks are enabled](https://github.com/mattermost/platform/blob/master/doc/integrations/webhooks/Incoming-Webhooks.md#enabling-incoming-webhooks).**


### Quick Install with Heroku

If you don't already have a Heroku account please go create one [here](https://www.heroku.com/) (it's free!).

1. Deploy integration to Heroku
 1. Fork the [mattermost-integration-gitlab](https://github.com/mattermost/mattermost-integration-gitlab) repository on GitHub by clicking _Fork_ in the top-right and selecting your account if it asks.
 1. Log in to [Heroku](https://www.heroku.com/) and go to your [dashboard](https://dashboard.heroku.com/apps).
 2. Click the `+` in the top-right corner to add a new _app_.
 3. Give your app a name and select your region, then click _Create App_.
 4. On the _Deploy_ screen, select _GitHub_ at the top.
 5. Use _Connect to GitHub_ to authorize Herkou to access your GitHub account.
 6. Select your account and type `gitlab-mattermost` into the _repo-name_ field, then click _Search_.
 7. Click the _Connect_ button next to your repository.
 8. Scroll to the bottom of the new page and under the _Manual deploy_ section click _Deploy Branch_, making sure the `master` branch is selected.
 9. Go to the _Settings_ tab and under the _Domains_ section copy the _Heroku Domain_.

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
