import acconeer.exptool as et
from acconeer.exptool.a111.algo import ModuleInfo


def main(module_info: ModuleInfo):
    arg_parse_kwargs = {} if module_info.multi_sensor else dict(num_sens=1)
    args = et.utils.ExampleArgumentParser(**arg_parse_kwargs).parse_args()
    et.utils.config_logging(args)

    if args.socket_addr:
        client = et.SocketClient(args.socket_addr)
    elif args.spi:
        client = et.SPIClient()
    else:
        port = args.serial_port or et.utils.autodetect_serial_port()
        client = et.UARTClient(port)

    client.squeeze = not module_info.multi_sensor

    sensor_config = module_info.sensor_config_class()
    processing_config = module_info.processing_config_class()
    sensor_config.sensor = args.sensors

    session_info = client.setup_session(sensor_config)

    pg_updater = module_info.pg_updater(sensor_config, processing_config, session_info)
    pg_process = et.PGProcess(pg_updater)
    pg_process.start()

    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session")

    processor = module_info.processor(sensor_config, processing_config, session_info)

    while not interrupt_handler.got_signal:
        info, sweep = client.get_next()
        plot_data = processor.process(sweep, info)

        if plot_data is not None:
            try:
                pg_process.put_data(plot_data)
            except et.PGProccessDiedException:
                break

    print("Disconnecting...")
    pg_process.close()
    client.disconnect()
