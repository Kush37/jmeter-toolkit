from jmeter_builder import *


def save(path, xml):
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    model = parse_har("Demo_Blaze_Phones_Home_AboutUs.har")

    jmx = create_empty_jmeter_script("HAR Test")
    print(jmx)

    jmx, tg_id = add_thread_group(jmx, "Load Test", 50, 30)
    print(jmx)

    for txn in model.transactions:
        jmx, txn_id = add_transaction_controller(jmx, tg_id, txn.name)

        for ex in txn.exchanges:
            jmx, sampler_id = add_http_sampler(jmx, txn_id, ex.request.name, ex.request.method, ex.request.url)
            jmx = add_header_manager(jmx, sampler_id, ex.request.headers)

    jmx = add_think_time_between_transactions(jmx, tg_id, 5000)
    print(jmx)
    save("output.jmx", jmx)


if __name__ == "__main__":
    main()
