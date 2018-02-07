from flask import Flask
from flask import render_template

app = Flask(__name__)

def get_db_connection():
    import sqlite3

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    conn_c = conn.cursor()
    return conn_c

def lookup_posts_for_template():
    import math

    conn_c = get_db_connection()
    conn_c.execute('SELECT * FROM posts ORDER BY post_date DESC')
    posts_info = conn_c.fetchall()

    num_of_columns = 3
    num_of_posts = float(len(posts_info))
    num_of_placeholders = int((num_of_columns*math.ceil(num_of_posts/num_of_columns)) - num_of_posts)

    for_template = {}
    for_template['posts_info']          = posts_info
    for_template['num_of_columns']      = num_of_columns
    for_template['num_of_posts']        = num_of_posts
    for_template['num_of_placeholders'] = num_of_placeholders

    return for_template

@app.route('/')
def home():
    for_template = lookup_posts_for_template()
    return render_template('home.html', posts_info=for_template['posts_info']
                                      , num_of_posts=for_template['num_of_posts']
                                      , num_of_columns=for_template['num_of_columns']
                                      , num_of_placeholders=for_template['num_of_placeholders'])

@app.route('/creativity')
def creativity():
    for_template = lookup_posts_for_template()
    return render_template('creativity.html', posts_info=for_template['posts_info']
                                            , num_of_posts=for_template['num_of_posts']
                                            , num_of_columns=for_template['num_of_columns']
                                            , num_of_placeholders=for_template['num_of_placeholders'])

@app.route('/activity')
def action():
    for_template = lookup_posts_for_template()
    return render_template('activity.html', posts_info=for_template['posts_info']
                                          , num_of_posts=for_template['num_of_posts']
                                          , num_of_columns=for_template['num_of_columns']
                                          , num_of_placeholders=for_template['num_of_placeholders'])

@app.route('/service')
def service():
    for_template = lookup_posts_for_template()
    return render_template('service.html', posts_info=for_template['posts_info']
                                         , num_of_posts=for_template['num_of_posts']
                                         , num_of_columns=for_template['num_of_columns']
                                         , num_of_placeholders=for_template['num_of_placeholders'])

@app.route('/post/<post_id>')
def post(post_id):
    # posts = ['this is the text for post 0', 'this is the text for post 1', 'this is the text for post 2']
    # return render_template('post.html', post_text=posts[int(post_id)])
    conn_c = get_db_connection()
    conn_c.execute('SELECT * FROM posts WHERE post_id=?', (post_id,))

    post_info = conn_c.fetchone()

    return render_template('post.html', post_text=post_info['post_text'],
                                        post_title=post_info['post_title'],
                                        post_date=post_info['post_date'],
                                        post_img_name=post_info['post_img_name'])

    # test = ('This', 'image_1.png')
    # test[0]
    # test = {'post_text': 'This',
    #         'post_img_name': 'image_1.png'}
    # test['post_text']


# SELECT *
# FROM posts
# WHERE (length(post_text) - LENGTH(replace(post_text, ' ', '')) + 1) > 2

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     import folium
#
#     center_location = [41.395412, 2.153868]
#     m_bw_zoomed = folium.Map(location=center_location, tiles='Stamen Toner',
#                              zoom_start=100, width=800, height=300)
#
#     center_marker = folium.Marker(center_location, popup='<b>You Are Here!<b/>',
#                                   icon=folium.Icon(color='green', icon='home'))
#     center_marker.add_to(m_bw_zoomed)
#
#     center_circle = folium.Circle(radius=100, location=center_location, color='pink', fill=True)
#     center_circle.add_to(m_bw_zoomed)
#
#     m_bw_zoomed.save('templates/map.html')
#
#     return render_template('hello.html', name=name)
