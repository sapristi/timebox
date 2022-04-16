# Configuration file

Timebox is configured with a yaml file. The file can have two top-level fields:
- `backups`: mapping of `Backup` (by name). Configuration for what to back-up, and where it should be stored.
- `config`: shared configuration values. If not provided, the default values will be used.

## Backup


- name[string] **required** 
  Unique name used to identify this backup. Inferred from the `backups` mapping.
- input[InputProvider] **required** 
- outputs[List[OutputProvider]] **required** 
- rotation[RotationProvider] **required** 

## Config


- log_level[DEBUG|INFO|WARNING|ERROR] (default: WARNING) 
- secrets_file[string] (default: None) 
  Path to a file containing secret values.
- notification[NotificationProvider] (default: None) 
  Specify which provider will be used to send notifications.
- use_secrets[boolean] (default: False) 
  Disables using external secrets. Secret values should be directly provided in the config file.

## Providers 

See [the dedicated page](/docs/providers.md)

# Examples


## example1.yaml

```yaml
backups:
  my_data:
    input:
      type: folder
      path: /my/data
    outputs:
      - type: folder
        path: /tmp
    rotation:
      type: simple
      days: 2

```

## example2.yaml

```yaml
backups:
  my_db:
    input:
      type: postgres
      database: my_db
    outputs:
      - type: rclone
        remote: my_bucket
        path: /my/db
    rotation:
      type: simple
      days: 10

config:
  log_level: INFO
  notification:
    type: webhook
    method: Post
    url: https://discord.com/api/channels/90CHANNEL_ID0458/messages
    headers:
      Authorization: Bot <SECRET>
    body:
      content: |
        **<SUMMARY>**

        <MESSAGE>
    secret: DISCORD_BOT_TOKEN


```