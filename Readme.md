# Timebox

Timebox is a small tools that helps you backup your files or databases. The backups can either be stored locally, or on the cloud (thanks to the awesome [rclone](https://rclone.org/)).

Timebox aims to stay simple, straightforward, and unobtrusive. 
 - The backup files are stored as is, which means you don't need timebox to retrieve them (this also means no incremental backup).
 - It does not rely on any kind of database. All necessary metadata are stored in the filenames.

Implementation wise, the goal is to 
 - provide a wrapper around existing system commands.
 - provide an easily extensible system.
 
## How to use

### Configuration

In order to use timebox, you will need to write a `yaml` configuration file. Here's an example configuration of such file:

```yaml
backups:
  my_db:
    input:
      type: postgres
      username: user
      database: my_db
      password: DB_PWD
    outputs:
      - type: folder
        path: /data/backups
    rotation:
      type: simple
      days: 30
config:
  secrets_file: .secrets
  notification:
    type: webhook
    method: Post
    url: https://discord.com/api/channels/908MYCHANNEL458/messages
    secret: DISCORD_BOT_TOKEN
    headers:
      Authorization: Bot <SECRET>
    body:
      content: |
        **<SUMMARY>**

        <MESSAGE>
```

Here you can see a configuration with a single backup. 
 - It takes as input a postgres database.
 - It has a single output, the local `/data/backups` folder.
 - Files will be kept for 30 days.
 - the file `.secrets` will be read to fetch sensitive values (`DB_PWD` and `DISCORD_BOT_TOKEN`)
 - once the backup is done, the webhook will be triggerd, posting a message on discord

The `.secrets` file is parsed with the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package; it's content could be e.g. 
```
DB_PWD=my_very_long_db_pwd
DISCORD_BOT_TOKEN=2d1BfqacR9SPLUiXfo4mMHwVn2IR4Kv208O8tZ2q
```

See also:
- **[the config file documentation](/docs/main.md)**
- **[the providers documentation](/docs/providers.md)**

### Execution

Timebox expects to be called daily for performing backups: `timebox -c /path/to/config.yaml run`.

You can also list files stored on the configured outputs:  `timebox -c /path/to/config.yaml ls`.

**Note***: the `rclone` output provider expects `rclone` to be already installed and configured.

Secret values will be fetched from the (optional) `secrets_file`, as well as from environment variables.

# Why another backup manager ?

I had a somewhat specific requirement, "decaying rotation" (more on that below), and none of the tools I found had exactly what I was looking for.

This project's name took inspiration from [blackbox](https://github.com/lemonsaurus/blackbox), another backup manager written in Python.


## Decaying rotation

The idea around decaying rotation is to keep a minimal number of backups, while keeping a long backup period. To do so, we have to keep some backups for a long time, while other will be short lived. This might be especially usefull when performing a backup of personal files, where you might realise you have deleted something usefull only a long time after the deletion has occured.

### Implementation

The method I found out was in fact the same as the [Tower of Hanoi roation scheme](https://en.wikipedia.org/wiki/Backup_rotation_scheme#Tower_of_Hanoi) (with some twists).

The specific implementation takes as input a `base`:

 - Each *2<sup>base</sup>* days, a new backup with a lifetime of *2<sup>base+1</sup>* days will be created.
 - Between two such backups, a new backup with a lifetime of *2<sup>base</sup>* days will be created.
 - We keep on creating backups in the remainging intervals, each time dividing the backup lifetime by two.
 
The following plots, computed for base 3 and 4, should give you a good idea of what is going on:

| base 3 | base 4 |
| ------------- |:-------------:|
| <img src="./notebooks/base3.png" alt="decaying backup, base 3" width="200"/> | <img src="./notebooks/base4.png" alt="decaying backup, base 4" width="200"/> |

This gives us a rotation strategy with the following property:
 
- For each *0 <= i <= base*, we have exactly **one** ([sometimes two?](https://xkcd.com/2248/)) backup that is between *2<sup>i</sup>* and *2<sup>i+1</sup>* days old.
- At all time, you have exactly *(base + 2)* backup files.

To give a practical example, you can have backups that span at least 256 days (and at most 512), while having only 10 backup files !
