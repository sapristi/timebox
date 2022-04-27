
# Providers

Providers gives timebox a lot of flexibity in its behaviour. When describing a
provider in the configuration, the `type` field is used to infer which class will
be parsed.

## InputProvider

Input providers are used to collect data to back up.


### FolderInputProvider

Creates a tar archive from a given folder.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "folder" | | |
| path | `string`| **required** |  | Path to the folder to compress. |
| compression | `gzip\|bzip2\|xz`| *default: `xz`* |  |  |
| exclude | `array`| *default: `None`* |  | Paths to exclude. |
| extra_args | `array`| *default: `None`* |  | Extra arguments to pass to the `tar` command. |


### PostgresInputProvider

Dumps the given postgres database, using the `pg_dump` command.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "postgres" | | |
| database | `string`| **required** |  |  |
| host | `string`| *default: `None`* |  |  |
| username | `string`| *default: `None`* |  |  |
| port | `string`| *default: `None`* |  |  |
| password | `string`| *default: `None`* | *Secret* |  |


### CommandInputProvider

Runs the given command. Use the `DESTFILE` environment variable as the target filename.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "command" | | |
| command | `array`| **required** |  |  |
| extension | `string`| *default: `None`* |  | Extension to associate with created files. |
| secret | `string`| *default: `None`* | *Secret* |  |
| secret_name | `string`| *default: `None`* |  | Environment variable name holding secret value. |
| expected_returncode | `integer`| *default: `0`* |  |  |
| env_extra | `object`| *default: `{}`* |  | Extra environment variables. |



## OutputProvider

Output providers are used to store backups.


### FolderOutputProvider

Stores backups in the given local folder.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "folder" | | |
| path | `string`| **required** |  |  |


### RCloneOutputProvider

Use rclone to send backups to pre-configured remotes.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "rclone" | | |
| remote | `string`| **required** |  |  |
| path | `string`| **required** |  |  |
| executable | `string`| *default: `rclone`* |  |  |



## RotationProvider

Rotation providers implement the logic to determine backups rotation.


### SimpleRotation

Keeps backups the given number of days.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "simple" | | |
| days | `integer`| **required** |  |  |


### PeriodRotation

Ensures backups are kept for each of the given periods.

For example, if you specify months=2, the backups made
on the first day of a month will be kept for 2 months.



| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "period" | | |
| days | `integer`| *default: `0`* |  |  |
| months | `integer`| *default: `0`* |  |  |
| years | `integer`| *default: `0`* |  |  |


### DecayingRotation

Keeps backups in a decaying fashion, allowing to cover a long timespan with a small number of backups.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "decaying" | | |
| base | `integer`| **required** |  |  |
| offset | `integer`| *default: `0`* |  |  |
| starting_point | `string`| *default: `1970-01-01`* |  |  |



## NotificationProvider

Notification providers are used to send notifications.


### WebhookNotificationProvider


Executes and HTTP request to the given url.

The provided `secret` can be used either in the `url`, or in the `headers`: use the string `<SECRET>` as a placeholder.

The strings `<SUMMARY>` and `<MESSAGE>` can be used as placeholders in the body for the report data.



| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "webhook" | | |
| url | `string`| **required** |  |  |
| method | `string`| *default: `POST`* |  |  |
| headers | `object`| *default: `{}`* |  |  |
| body | `object`| *default: `{}`* |  |  |
| secret | `string`| *default: `None`* | *Secret* |  |


### CommandNotificationProvider

Run a system command. `SUMMARY`, `MESSAGE` and `HAS_ERROR` are provided as environment variables.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "command" | | |
| command | `array`| **required** |  |  |


### SMTPNotificationProvider

Email notification.


| field name | type | value | secret  | doc |
| ---        | ---  | --- | ---     | --- |
| type       |  | "smtp" | | |
| server | `string`| **required** |  |  |
| sender_email | `string`| **required** |  |  |
| password | `string`| **required** | *Secret* |  |
| recipient_email | `string`| **required** |  |  |
| port | `integer`| *default: `465`* |  |  |



