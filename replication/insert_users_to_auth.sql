CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
INSERT INTO auth.users VALUES ('82fafaad-f528-4d2c-95b4-82d37889c8cd', 'help', 'help@mail.local', 'password', uuid_generate_v4(), NOW(), NOW());
INSERT INTO auth.users_info VALUES (uuid_generate_v4(), '82fafaad-f528-4d2c-95b4-82d37889c8cd', 'help', 'help!', 'Europe/Moscow', NOW(), NOW());

INSERT INTO auth.users VALUES ('82fafaad-f528-4d2c-95b4-82d37889c8dd', 'help1', 'help1@mail.local', 'password1', uuid_generate_v4(), NOW(), NOW());
INSERT INTO auth.users_info VALUES (uuid_generate_v4(), '82fafaad-f528-4d2c-95b4-82d37889c8dd', 'help1', 'help1!', 'Indian/Mauritius', NOW(), NOW());

INSERT INTO auth.users VALUES ('82fafaad-f528-4d2c-95b4-82d37889c8cc', 'help2', 'help2@mail.local', 'password2', uuid_generate_v4(), NOW(), NOW());
INSERT INTO auth.users_info VALUES (uuid_generate_v4(), '82fafaad-f528-4d2c-95b4-82d37889c8cc', 'help2', 'help2!', 'US/Samoa', NOW(), NOW());
