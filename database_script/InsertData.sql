use sleipnir;

INSERT INTO tenants (`tenant_name`) VALUES
('Test1'),
('Test2');

INSERT INTO users (`username`, `password`, `email`, `tenant_id`) VALUES
('lorak', 'lorak', 'lora.kang@akoa.com', 1),
('lorakang', 'lorakang', 'lora.kang@new-innovation.com', 2);


INSERT INTO rights (`right`) VALUES
('admin'),
('use');

INSERT INTO users_rights (`user_id`, `right_id`) VALUES
('1', '1'),
('1', '2'),
('2', '2');