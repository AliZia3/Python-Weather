from tkinter import *
import requests


# Returns information as list
def format_response(weather_info):
    try:
        city = weather_info['name']
        country = weather_info['sys']['country']
        weather_cond = weather_info['weather'][0]['main']
        weather_desc = weather_info['weather'][0]['description']
        temp = weather_info['main']['temp']
        feel_like = weather_info['main']['feels_like']
        windspeed = weather_info['wind']['speed']

        result = [city, country, str(temp), weather_cond, weather_desc, str(feel_like), str(windspeed)]
        weather_result = result[3]
        change_icon(weather_result)
    except:
        result = 0

    return result


def change_icon(weather_result):
    path = 'C:/Python_Projects/Weather_App/App_Files/Images/'
    file_type = '.png'

    weather_icon = path + weather_result + file_type

    try:
        bg_img.configure(file=weather_icon)
    except:
        bg_img.configure(file='')


# Outputs the results from format_response function into the label widgets to display info
def get_weather(city):
    weather_key = '74087a43755a584e6bf15cc2a7edf687'
    url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {"APPID": weather_key,
              'q': city,
              'units': 'metric'}
    response = requests.get(url, params=params)
    weather_info = response.json()
    final_result = format_response(weather_info)

    if final_result == 0:
        temp_label.configure(text="Problem Retrieving Information", font=font)
        location_label.configure(text='Error')

        for i in output_result:
            i.configure(text='?')

    else:
        temp_label.configure(text=(final_result[2] + '°C'), font=temp_font)
        location_label.configure(text=final_result[0] + ', ' + final_result[1])

        x = 3
        for i in output_result:
            i.configure(text=final_result[x])
            x += 1


# Entry field content is cleared when it is clicked
def click(event):
    entry.configure(state=NORMAL)
    entry.delete(0, END)
    entry.unbind('<Button-1>', clicked)
    entry.configure(fg="black")


# =========================================================
# GUI

# Initial Variables
root = Tk()
root.geometry('700x500')
root.title("Weather")
root.iconbitmap("C:/Python_Projects/Weather_App/App_Files/App_Icon.ico")
text_fg = "white"
entry_fg = "gray"
canvas_bg = '#87CEEB'
frame_bg = '#1d3863'
font = "Arial, 14"
temp_font = "Arial, 50"
initial_options = ['Conditions:', 'Description:', 'Feels like(°C):', 'Wind Speed(m/s):']
output_result = []
temp_initial = "..."
location_initial = '(City, Country)'
rely = 0.6
output_relx = 0.5

canvas = Canvas(root, bg=canvas_bg)
canvas.place(relwidth=1, relheight=1)

outer_frame = Frame(root, bg=frame_bg)
outer_frame.place(relwidth=0.98, relheight=0.96, relx=0.01, rely=0.02)

# =========================================================================

# Frame that contains all widgets that are used for searching
search_frame = Frame(outer_frame, bg=frame_bg)
search_frame.place(relheight=0.06, relwidth=0.6, relx=0.2, rely=0.05)

entry = Entry(search_frame, font=font, fg=entry_fg)
entry.insert(0, "City, Country (London, UK)")
entry.place(relheight=1, relwidth=0.65)
clicked = entry.bind('<Button-1>', click)

search_btn = Button(search_frame, text='Search', font=font, command=lambda: get_weather(entry.get()))
search_btn.place(relheight=1, relwidth=0.3, relx=0.7)

# ========================================================================

# Frame where all information is displayed
output_frame = Frame(outer_frame, bg=frame_bg)
output_frame.place(relwidth=0.5, relheight=0.7, relx=0.25, rely=0.15)

temp_label = Label(output_frame, text=temp_initial, fg=text_fg, bg=frame_bg, font=temp_font)
temp_label.place(relwidth=1, relheight=0.2)

location_label = Label(output_frame, text=location_initial, fg=text_fg, bg=frame_bg, font=font)
location_label.place(relwidth=1, relheight=0.1, rely=0.2)

for i in initial_options:
    initial_output = Label(output_frame, text=i, fg=text_fg, bg=frame_bg, font=font, justify='left', anchor='nw')
    initial_output.place(relwidth=0.5, relheight=0.1, rely=rely)
    rely += 0.1
    rounded_rely = round(rely, 2)
    if rounded_rely == 1.0:
        rely = 0.6

for i in initial_options:
    output = Label(output_frame, fg=text_fg, bg=frame_bg, font=font, justify='right', anchor='ne')
    output.place(relwidth=0.5, relheight=0.1, rely=rely, relx=output_relx)
    output_result.append(output)
    rely += 0.1
# ============================================================================

# Displays weather icon
bg_img = PhotoImage(file='')
bg_label = Label(output_frame, image=bg_img, bg=frame_bg)
bg_label.place(relwidth=0.2, relheight=0.2, rely=0.35, relx=0.4)

root.mainloop()
