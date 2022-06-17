from flask import Blueprint, redirect, render_template, request, flash, url_for
from app import db
from models import Course, Category, User, Review
from tools import CoursesFilter, ImageSaver
from flask_login import current_user

bp = Blueprint('courses', __name__, url_prefix='/courses')

PER_PAGE = 4

COURSE_PARAMS = ['author_id', 'name', 'category_id', 'short_desc', 'full_desc']
REVIEW_PARAMS = ['rating', 'text']

def params(param):
    return {p: request.form.get(p) for p in param }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids')
    }

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    courses = CoursesFilter(**search_params()).perform()
    pagination = courses.paginate(page, PER_PAGE)
    courses = pagination.items

    categories = Category.query.all()

    return render_template('courses/index.html', 
                            courses=courses, 
                            categories=categories,
                            pagination=pagination,
                            search_params=search_params()
                            )
                            
@bp.route('/new')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('courses/new.html', 
                            categories=categories, 
                            users=users
                            )

@bp.route('/create', methods=['POST'])
def create():

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()

    course = Course(**params(COURSE_PARAMS), background_image_id = img.id)
    db.session.add(course)
    db.session.commit()

    flash(f'Курс {course.name} был успешно создан.')
    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = Course.query.get(course_id)
    reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.created_at.desc()).limit(5)
    
    curr_review = None
    if current_user.is_authenticated:
        curr_review = Review.query.filter(Review.course_id == course_id).filter(Review.user_id == current_user.id).first()

    return render_template('courses/show.html', course=course, reviews=reviews, curr_review=curr_review)

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.created_at.desc())
    sort_type = request.args.get('filters')

    if sort_type == 'new_first': 
        reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.created_at.desc())
    elif sort_type == 'old_first': 
        reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.created_at.asc())
    elif sort_type == 'pos_first': 
        reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.rating.desc())
    elif sort_type == 'neg_first': 
        reviews = Review.query.filter(Review.course_id == course_id).order_by(Review.rating.asc())


    pagination = reviews.paginate(page, PER_PAGE)
    reviews = pagination.items

    curr_review = None
    if current_user.is_authenticated:
        curr_review = Review.query.filter(Review.course_id == course_id).filter(Review.user_id == current_user.id).first()


    return render_template('courses/reviews.html', reviews=reviews, course_id=course_id, pagination=pagination, curr_review=curr_review)

@bp.route('/<int:course_id>/reviews/create', methods=['POST'])
def create_review(course_id):
    new_review = Review(**params(REVIEW_PARAMS), course_id=course_id, user_id=current_user.id)
    db.session.add(new_review)

    course = Course.query.get(course_id)
    course.rating_num += 1
    course.rating_sum += int(new_review.rating)

    db.session.commit()
    flash(f'Комментарий был успешно создан.')

    return redirect(url_for('courses.show', course_id=course_id))