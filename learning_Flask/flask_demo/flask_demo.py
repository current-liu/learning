from flask import Flask, url_for, render_template, request, make_response, abort, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/hello/<name>')
def hello_world(name=None):
    cookie_request = request.cookies.get('u')
    resp = make_response(render_template('hello.html', name=name, cookie_request=cookie_request))
    resp.set_cookie("u", "u_")
    return resp


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/')
def projects():
    searchword = request.args.get('id', '')
    return 'The project page id = ' + str(searchword)


@app.route('/u/<username>')
def profile(username):
    pass


@app.route('/about')
def about():
    return url_for('profile', username='lc', _external=True)


@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return "please login"
    # abort(401)


@app.errorhandler(404)
def page_not_found(error):
    return 'page_not_found', 404


if __name__ == '__main__':
    app.run()
