from flask import Flask
from flask import render_template
from flask import request

application = Flask(__name__)

def get_db_connection():
    import sqlite3

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    conn_c = conn.cursor()
    return conn_c

def lookup_posts_for_template(category_name, query=None):
    import math

    conn_c = get_db_connection()

    posts_query = 'SELECT * FROM posts p'
    if category_name not in ['home', 'search']:
        posts_query += ' INNER JOIN post_categories pc ON p.post_id = pc.post_id AND pc.category = ?'
    if category_name == 'search':
        posts_query += ' WHERE post_text LIKE ?'
    posts_query += ' ORDER BY post_date DESC'

    if category_name not in ['home', 'search']:
        conn_c.execute(posts_query, (category_name,))
    elif category_name == 'search':
        conn_c.execute(posts_query, ('%' + query + '%',))
    else:
        conn_c.execute(posts_query)

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

@application.route('/')
def home():
    for_template = lookup_posts_for_template('home')
    return render_template('home.html', posts_info=for_template['posts_info']
                                      , num_of_posts=for_template['num_of_posts']
                                      , num_of_columns=for_template['num_of_columns']
                                      , num_of_placeholders=for_template['num_of_placeholders'])

@application.route('/creativity')
def creativity():
    for_template = lookup_posts_for_template('creativity')
    return render_template('creativity.html', posts_info=for_template['posts_info']
                                            , num_of_posts=for_template['num_of_posts']
                                            , num_of_columns=for_template['num_of_columns']
                                            , num_of_placeholders=for_template['num_of_placeholders'])

@application.route('/activity')
def action():
    for_template = lookup_posts_for_template('activity')
    return render_template('activity.html', posts_info=for_template['posts_info']
                                          , num_of_posts=for_template['num_of_posts']
                                          , num_of_columns=for_template['num_of_columns']
                                          , num_of_placeholders=for_template['num_of_placeholders'])

@application.route('/service')
def service():
    for_template = lookup_posts_for_template('service')
    return render_template('service.html', posts_info=for_template['posts_info']
                                         , num_of_posts=for_template['num_of_posts']
                                         , num_of_columns=for_template['num_of_columns']
                                         , num_of_placeholders=for_template['num_of_placeholders'])

@application.route('/search')
def search():
    query = request.args.get('q')
    for_template = lookup_posts_for_template('search', query)
    return render_template('search.html', posts_info=for_template['posts_info']
                                        , num_of_posts=for_template['num_of_posts']
                                        , num_of_columns=for_template['num_of_columns']
                                        , num_of_placeholders=for_template['num_of_placeholders'])

@application.route('/post/<post_id>')
def post(post_id):
    # posts = ['this is the text for post 0', 'this is the text for post 1', 'this is the text for post 2']
    # return render_template('post.html', post_text=posts[int(post_id)])
    conn_c = get_db_connection()

    conn_c.execute('SELECT * FROM posts WHERE post_id=?', (post_id,))
    post_info = conn_c.fetchone()

    conn_c.execute('SELECT * FROM post_images WHERE post_id=? ORDER BY img_order', (post_id,))
    imgs_info = conn_c.fetchall()
    num_imgs  = len(imgs_info)

    return render_template('post.html', post_text=post_info['post_text'],
                                        post_title=post_info['post_title'],
                                        post_date=post_info['post_date'],
                                        post_imgs=imgs_info,
                                        num_imgs=num_imgs)

    # test = ('This', 'image_1.png')
    # test[0]
    # test = {'post_text': 'This',
    #         'post_img_name': 'image_1.png'}
    # test['post_text']


# SELECT *
# FROM posts
# WHERE (length(post_text) - LENGTH(replace(post_text, ' ', '')) + 1) > 2

# @application.route('/hello/')
# @application.route('/hello/<name>')
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

if __name__ == "__main__":
    application.run()
