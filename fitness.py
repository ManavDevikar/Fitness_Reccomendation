import tkinter as tk
from tkinter import messagebox
import requests

class FitnessTracker:
    def __init__(self, current_weight, target_weight, height, age, gender, activity_level, diet_preference):
        self.current_weight = current_weight
        self.target_weight = target_weight
        self.height = height
        self.age = age
        self.gender = gender
        self.activity_level = activity_level
        self.diet_preference = diet_preference.lower()
        self.goal = None
        self.caloric_intake = 0
        self.daily_calories = self.calculate_daily_calories()
        self.fitness_plan = None

    def calculate_bmr(self):
        # Basic Metabolic Rate (BMR) Calculation
        if self.gender == 'male':
            bmr = 88.362 + (13.397 * self.current_weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            bmr = 447.593 + (9.247 * self.current_weight) + (3.098 * self.height) - (4.330 * self.age)
        return bmr

    def calculate_daily_calories(self):
        # Calculate calories based on activity level
        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        bmr = self.calculate_bmr()
        return bmr * activity_factors[self.activity_level]

    def set_goal(self, goal):
        self.goal = goal.lower()
        if self.goal == 'lose weight':
            self.caloric_intake = self.daily_calories - 500  # 500-calorie deficit
        elif self.goal == 'gain weight':
            self.caloric_intake = self.daily_calories + 500  # 500-calorie surplus
        else:
            raise ValueError("Invalid goal! Please choose 'lose weight' or 'gain weight'.")

    def log_progress(self, calories_consumed):
        if self.goal == 'lose weight' and calories_consumed < self.caloric_intake:
            return f"Great! You’re on track with a caloric deficit of {self.caloric_intake - calories_consumed:.2f} kcal."
        elif self.goal == 'gain weight' and calories_consumed > self.caloric_intake:
            return f"Awesome! You’re on track with a caloric surplus of {calories_consumed - self.caloric_intake:.2f} kcal."
        else:
            return "You need to adjust your intake to meet your goal."

    def suggest_diet_plan(self):
        # Vegetarian Diet Plan
        if self.diet_preference == 'veg':
            if self.goal == 'lose weight':
                return """Suggested Vegetarian Diet Plan for Weight Loss:
                - Breakfast: Oatmeal with almonds and fruit
                - Lunch: Lentil soup with whole-grain bread
                - Snacks: Carrots, hummus, or a small handful of nuts
                - Dinner: Quinoa salad with tofu and veggies
                - Drinks: Green tea, water"""
            elif self.goal == 'gain weight':
                return """Suggested Vegetarian Diet Plan for Weight Gain:
                - Breakfast: Smoothie with banana, peanut butter, and almond milk
                - Lunch: Brown rice with chickpeas and avocado
                - Snacks: Cheese sandwich or protein-rich snacks
                - Dinner: Paneer curry with whole-wheat naan and lentils
                - Drinks: Milk, protein shakes"""
        
        # Non-Vegetarian Diet Plan
        elif self.diet_preference == 'nonveg':
            if self.goal == 'lose weight':
                return """Suggested Non-Vegetarian Diet Plan for Weight Loss:
                - Breakfast: Scrambled eggs with spinach and avocado
                - Lunch: Grilled chicken salad with olive oil and quinoa
                - Snacks: Greek yogurt or boiled eggs
                - Dinner: Grilled fish with steamed vegetables
                - Drinks: Water, green tea"""
            elif self.goal == 'gain weight':
                return """Suggested Non-Vegetarian Diet Plan for Weight Gain:
                - Breakfast: Omelette with whole grain toast and avocado
                - Lunch: Chicken breast with brown rice and veggies
                - Snacks: Peanut butter on whole-grain bread, or a protein shake
                - Dinner: Steak or salmon with sweet potatoes and veggies
                - Drinks: Whole milk, smoothies with protein powder"""

    def generate_workout_plan(self):
        # A 6-day workout plan for both weight loss and weight gain
        if self.goal == 'lose weight':
            return """6-Day Workout Plan for Weight Loss:
            Day 1: Cardio (Running or Cycling for 30 minutes)
            Day 2: Full Body Strength Training (Squats, Deadlifts, Push-ups)
            Day 3: Cardio (HIIT - 20 minutes)
            Day 4: Lower Body Strength Training (Leg Press, Lunges, Step-ups)
            Day 5: Cardio (Swimming or Jogging - 30 minutes)
            Day 6: Upper Body Strength Training (Pull-ups, Rows, Bench Press)
            Day 7: Rest"""
        elif self.goal == 'gain weight':
            return """6-Day Workout Plan for Weight Gain:
            Day 1: Chest and Triceps (Bench Press, Tricep Dips, Push-ups)
            Day 2: Back and Biceps (Deadlifts, Pull-ups, Barbell Rows)
            Day 3: Legs (Squats, Leg Press, Lunges)
            Day 4: Shoulders (Overhead Press, Lateral Raises, Shrugs)
            Day 5: Arms (Bicep Curls, Tricep Extensions, Hammer Curls)
            Day 6: Full Body Strength Training (Compound Movements: Squats, Deadlifts, Bench Press)
            Day 7: Rest"""

    def set_fitness_plan(self, plan):
        if plan == 'cardio':
            self.fitness_plan = "Cardio-based plan: 30 minutes of running, 20 minutes of cycling."
        elif plan == 'strength':
            self.fitness_plan = "Strength-based plan: 4 sets of squats, 4 sets of deadlifts, and 4 sets of bench press."
        elif plan == 'balanced':
            self.fitness_plan = "Balanced plan: 20 minutes of cardio and 30 minutes of strength training."
        else:
            raise ValueError("Invalid plan! Choose 'cardio', 'strength', or 'balanced'.")
        return self.fitness_plan

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")
        
        # Create labels and entry fields for user input
        self.create_user_input_fields()

    def create_user_input_fields(self):
        # Labels and Inputs
        tk.Label(self.root, text="Current Weight (kg):").grid(row=0, column=0, padx=10, pady=5)
        self.current_weight_entry = tk.Entry(self.root)
        self.current_weight_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Target Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
        self.target_weight_entry = tk.Entry(self.root)
        self.target_weight_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Height (cm):").grid(row=2, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(self.root)
        self.height_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Age:").grid(row=3, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Gender (male/female):").grid(row=4, column=0, padx=10, pady=5)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Activity Level (sedentary/light/moderate/active/very active):").grid(row=5, column=0, padx=10, pady=5)
        self.activity_level_entry = tk.Entry(self.root)
        self.activity_level_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Diet Preference (veg/nonveg):").grid(row=6, column=0, padx=10, pady=5)
        self.diet_preference_entry = tk.Entry(self.root)
        self.diet_preference_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Goal (lose weight/gain weight):").grid(row=7, column=0, padx=10, pady=5)
        self.goal_entry = tk.Entry(self.root)
        self.goal_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Calories Consumed Today:").grid(row=8, column=0, padx=10, pady=5)
        self.calories_entry = tk.Entry(self.root)
        self.calories_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Preferred Fitness Plan (cardio/strength/balanced):").grid(row=9, column=0, padx=10, pady=5)
        self.plan_entry = tk.Entry(self.root)
        self.plan_entry.grid(row=9, column=1, padx=10, pady=5)

        # Submit and Reset buttons
        tk.Button(self.root, text="Submit", command=self.calculate_fitness).grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Reset", command=self.reset_fields).grid(row=11, column=0, columnspan=2, padx=10, pady=5)

        # Additional button for food nutrition lookup
        tk.Button(self.root, text="Check Food Nutrition", command=self.open_food_nutrition_window).grid(row=12, column=0, columnspan=2, padx=10, pady=5)

    def calculate_fitness(self): 
        try:
            # Get user inputs
            current_weight = float(self.current_weight_entry.get())
            target_weight = float(self.target_weight_entry.get())
            height = float(self.height_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_entry.get().lower()
            activity_level = self.activity_level_entry.get().lower()
            diet_preference = self.diet_preference_entry.get().lower()
            goal = self.goal_entry.get().lower()
            calories_today = float(self.calories_entry.get())
            fitness_plan = self.plan_entry.get().lower()

            # Create fitness tracker object
            tracker = FitnessTracker(current_weight, target_weight, height, age, gender, activity_level, diet_preference)
            tracker.set_goal(goal)

            # Get daily caloric intake and log progress
            summary = tracker.log_progress(calories_today)

            # Get diet plan and workout plan
            diet_plan = tracker.suggest_diet_plan()
            workout_plan = tracker.generate_workout_plan()

            # Get additional fitness plan
            fitness_plan_summary = tracker.set_fitness_plan(fitness_plan)

            # Calculate calories for weight loss and weight gain
            calories_for_weight_loss = tracker.daily_calories - 500
            calories_for_weight_gain = tracker.daily_calories + 500

            # Show summary
            messagebox.showinfo("Fitness Summary", f"{summary}\n\nDiet Plan:\n{diet_plan}\n\nWorkout Plan:\n{workout_plan}\n\n"
                                                   f"Fitness Plan:\n{fitness_plan_summary}\n\n"
                                                   f"Your estimated daily caloric need to maintain your current weight is {tracker.daily_calories:.2f} kcal.\n"
                                                   f"To lose weight, consume around {calories_for_weight_loss:.2f} kcal/day.\n"
                                                   f"To gain weight, consume around {calories_for_weight_gain:.2f} kcal/day.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def reset_fields(self):
        # Clear all input fields
        self.current_weight_entry.delete(0, tk.END)
        self.target_weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.activity_level_entry.delete(0, tk.END)
        self.diet_preference_entry.delete(0, tk.END)
        self.goal_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.plan_entry.delete(0, tk.END)

    def open_food_nutrition_window(self):
        # Create a new window for food nutrition lookup
        self.food_window = tk.Toplevel(self.root)
        self.food_window.title("Food Nutrition Lookup")

        tk.Label(self.food_window, text="Enter Food Name:").grid(row=0, column=0, padx=10, pady=5)
        self.food_entry = tk.Entry(self.food_window)
        self.food_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.food_window, text="Get Nutrition Info", command=self.get_nutrition_info).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def get_nutrition_info(self):
        try:
            food_name = self.food_entry.get()
            if not food_name:
                raise ValueError("Please enter a food name!")

            # Make a request to the Nutritionix API
            app_id = '3dd82dac'
            app_key = 'a4d77b54683135e5c23c8dec50126969'
            url = f"https://trackapi.nutritionix.com/v2/natural/nutrients"
            headers = {
                "x-app-id": app_id,
                "x-app-key": app_key,
                "Content-Type": "application/json"
            }
            data = {"query": food_name}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                food_data = response.json()
                nutrients = food_data['foods'][0]
                calories = nutrients.get('nf_calories', 'N/A')
                protein = nutrients.get('nf_protein', 'N/A')
                fat = nutrients.get('nf_total_fat', 'N/A')
                carbs = nutrients.get('nf_total_carbohydrate', 'N/A')

                # Display the nutritional information
                nutrition_info = f"Food: {food_name}\nCalories: {calories} kcal\nProtein: {protein} g\nFat: {fat} g\nCarbs: {carbs} g"
                messagebox.showinfo("Nutrition Info", nutrition_info)
            else:
                raise ValueError("Failed to fetch data. Check your API keys or food name.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Main Driver
if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
