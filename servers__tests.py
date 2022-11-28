#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, Server, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries_with_arg(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_returns_proper_entries_without_arg(self):
        products = [Product('B432', 50), Product('BB432', 100), Product('BbB432', 100), Product('BB789', 90),
                    Product('B789', 70)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries()
            self.assertEqual(Counter([products[4], products[0]]), Counter(entries))

    def test_too_many_results_list(self):
        products = [Product('Ab123', 50), Product('AA123', 100), Product('Aa123', 100), Product('AA234', 90),
                    Product('Aa123', 70), Product('Ab123', 70), Product('ABc123', 70)]
        server = ListServer(products)
        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries(2)

    def test_too_many_results_dict(self):
        products = [Product('AB123', 50), Product('AA123', 100), Product('Aa123', 100), Product('AA234', 90),
                    Product('Aa123', 70), Product('Ab123', 70), Product('ABc123', 70)]
        server = ListServer(products)
        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries(2)

    def test_empty_results(self):
        products = [Product('Ab123', 50), Product('AA123', 100), Product('AaA123', 100), Product('AA234', 90),
                    Product('Aa123', 70)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(1)
            self.assertEqual([], entries)

    def test_is_sorted_1(self):
        products = [Product('A123', 50), Product('AA123', 100), Product('AaA123', 100), Product('AA234', 90),
                    Product('Aa123', 70)]
        server = ListServer(products)
        results = server.get_entries(2)
        self.assertEqual([products[4], products[3], products[1]], results)

    def test_is_sorted_2(self):
        products = [Product('B123', 50), Product('Bb123', 50), Product('Bb234', 50), Product('BB123', 50)]
        server = ListServer(products)
        results = server.get_entries(2)
        self.assertEqual([products[1], products[2], products[3]], results)

class ProductTest(unittest.TestCase):

    def test_product_append(self):
        Product('Ff354', 200)
        Product('Gg35', 1000)

    def test_product_eq(self):
        self.assertEqual(Product('Ff354', 200), Product('Gg35', 1000))

    def test_product_error(self):
        with self.assertRaises(ValueError):
            Product('x4x4xx', 5)
        with self.assertRaises(ValueError):
            Product('2AAA', 10)
        with self.assertRaises(ValueError):
            Product('288', 'GF')
        with self.assertRaises(ValueError):
            Product('ilk5', -50)
        with self.assertRaises(ValueError):
            Product('s0n11', 4)



class ClientTest(unittest.TestCase):
    def test_total_price_proper_execution(self):
        products = [Product('PP234', 50), Product('PP235', 50)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(100, client.get_total_price(2))

    def test_total_price_but_exception(self):
        products = []
        for i in range(Server.n_max_returned_entries + 1):
            products.append(Product('Aa123', 100))
        server = ListServer(products)
        client = Client(server)
        self.assertEqual(-100, client.get_total_price(2))

    def test_total_price_if_no_entries(self):
        products = [Product('A123', 50), Product('AA123', 100), Product('AA234', 90), Product('Aa123', 70)]
        server = ListServer(products)
        client = Client(server)
        self.assertEqual(0, client.get_total_price(3))


if __name__ == '__main__':
    unittest.main()