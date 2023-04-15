# Your name: Sincheol Yang
# Your student id:9695 5598
# Your email: sincheol@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    data = cursor.fetchall()
    rest_data = {}
    for row in data:
        rest_name = row[0]
        category = row[1]
        building = row[2]
        rating = row[3]
        if rest_name not in rest_data:
            rest_data[rest_name] = {"category": category, "building": building, "rating": rating}
    return rest_data


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) FROM restaurants GROUP BY category")
    data = cursor.fetchall()
    rest_categories = {}
    for row in data:
        rest_categories[row[0]] = row[1]
    plt.bar(rest_categories.keys(), rest_categories.values())
    plt.xticks(rotation=45)
    plt.title("Number of Restaurants per Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.show()
    return rest_categories

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    pass

#EXTRA CREDIT
def get_highest_rating(db):
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Get the highest-rated restaurant category and its average rating
    c.execute("SELECT category, AVG(rating) as avg_rating FROM restaurants GROUP BY category ORDER BY avg_rating DESC LIMIT 1")
    category_data = c.fetchone()

    # Get the highest-rated building and its average rating
    c.execute("SELECT building, AVG(rating) as avg_rating FROM restaurants GROUP BY building ORDER BY avg_rating DESC LIMIT 1")
    building_data = c.fetchone()

    # Create bar chart for restaurant categories
    c.execute("SELECT category, AVG(rating) as avg_rating FROM restaurants GROUP BY category ORDER BY avg_rating DESC")
    category_rows = c.fetchall()
    categories = [row[0] for row in category_rows]
    avg_ratings = [row[1] for row in category_rows]

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    axs[0].barh(categories, avg_ratings)
    axs[0].set_title('Average ratings by restaurant category')
    axs[0].set_xlabel('Average rating')
    axs[0].set_ylabel('Restaurant category')
    axs[0].invert_yaxis()

    # Create bar chart for buildings
    c.execute("SELECT building, AVG(rating) as avg_rating FROM restaurants GROUP BY building ORDER BY avg_rating DESC")
    building_rows = c.fetchall()
    buildings = [row[0] for row in building_rows]
    avg_ratings = [row[1] for row in building_rows]

    axs[1].barh(buildings, avg_ratings)
    axs[1].set_title('Average ratings by building')
    axs[1].set_xlabel('Average rating')
    axs[1].set_ylabel('Building')
    axs[1].invert_yaxis()

    plt.tight_layout()
    plt.show()

    conn.close()

    return [(category_data[0], category_data[1]), (building_data[0], building_data[1])]


#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
