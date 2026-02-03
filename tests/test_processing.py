from src.processing import filter_by_state, sort_by_date


def test_filter_by_state():
    def setUp(self):
        """Создание общего набора данных для тестирования"""
        self.items = [
            {'name': 'Item 1', 'state': 'active'},
            {'name': 'Item 2', 'state': 'inactive'},
            {'name': 'Item 3', 'state': 'active'},
            {'name': 'Item 4', 'state': 'pending'},
            {'name': 'Item 5', 'state': 'inactive'},
        ]

    def test_filter_active_state(self):
        result = filter_by_state(self.items, 'active')
        expected = [
            {'name': 'Item 1', 'state': 'active'},
            {'name': 'Item 3', 'state': 'active'}
        ]
        self.assertEqual(result, expected)

    def test_filter_inactive_state(self):
        result = filter_by_state(self.items, 'inactive')
        expected = [
            {'name': 'Item 2', 'state': 'inactive'},
            {'name': 'Item 5', 'state': 'inactive'}
        ]
        self.assertEqual(result, expected)

    def test_filter_pending_state(self):
        result = filter_by_state(self.items, 'pending')
        expected = [
            {'name': 'Item 4', 'state': 'pending'}
        ]
        self.assertEqual(result, expected)

    def test_filter_nonexistent_state(self):
        result = filter_by_state(self.items, 'completed')
        expected = []
        self.assertEqual(result, expected)

    def test_empty_list(self):
        result = filter_by_state([], 'active')
        expected = []
        self.assertEqual(result, expected)

    def test_invalid_input_type(self):
        with self.assertRaises(ValueError):
            filter_by_state("not a list", 'active')


def test_sort_by_date():
    def setUp(self):
        """Создание общего набора данных для тестирования"""
        self.items = [
            {'name': 'Item 1', 'date': '2023-10-25'},
            {'name': 'Item 2', 'date': '2023-10-20'},
            {'name': 'Item 3', 'date': '2023-10-25'},
            {'name': 'Item 4', 'date': '2023-09-15'},
            {'name': 'Item 5', 'date': '2023/10/20'}
        ]

    def test_sort_ascending(self):
        sorted_items = sort_by_date(self.items, reverse=False)
        expected_dates = [
            '2023/10/20',
            '2023-10-20',
            '2023-10-25',
            '2023-10-25',
            '2023-09-15'
        ]
        self.assertEqual([item['date'] for item in sorted_items], expected_dates)

    def test_sort_descending(self):
        sorted_items = sort_by_date(self.items, reverse=True)
        expected_dates = [
            '2023-10-25',
            '2023-10-25',
            '2023-10-20',
            '2023/10/20',
            '2023-09-15'
        ]
        self.assertEqual([item['date'] for item in sorted_items], expected_dates)

    def test_sort_with_identical_dates(self):
        items = [
            {'name': 'Item A', 'date': '2023-10-25'},
            {'name': 'Item B', 'date': '2023-10-25'}
        ]
        sorted_items = sort_by_date(items, reverse=False)
        self.assertEqual(sorted_items[0]['name'], 'Item A')  # Проверяем, что порядок не меняется

    def test_invalid_date_format(self):
        self.items[-1]['date'] = 'invalid_date'
        with self.assertRaises(ValueError):
            sort_by_date(self.items)

    def test_missing_date(self):
        self.items[0]['date'] = None
        with self.assertRaises(ValueError):
            sort_by_date(self.items)

    def test_empty_list(self):
        result = sort_by_date([])
        self.assertEqual(result, [])
