Representation of log tool.

    The proper way to get an instance of this class is to call
    logging.Logger.

    Provide a tool for write runtime log to the file. Accepts several
    arguments:

    :param name: log file name
    :param is_add_stream_handler: Whether to print the log to the console
    :param do_not_use_color_handler: Whether forbid log color.
    :param log_path: file log path.
    :param log_file_size: Limit log file size.
    :param log_file_handler_type: Select log header type .
    :param formatter_template: Fixed log template.
    