import run_queries as rq
import numpy as np
import asyncio

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped
page_size = 10

def get_review_info(page_size, offset):
    reviews_query = f'''
        MATCH p=(s)-[r:reviewed_by]->(e) RETURN id(s), id(e) skip {offset} LIMIT {page_size}
    '''
    reviews = rq.make_request(reviews_query,'gathering data')
    return [ (i['row'][0], i['row'][1]) for i in reviews['results'][0]['data']]

def get_reviews_formatted(reviews):
    review_text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
    decision = "Approved" if np.random.rand() < 0.98 else "Denied"
    return '[{}]'.format(','.join([f'{{start: {i[0]},end: {i[1]},review: "{review_text}", decision: "{decision}"}}' for i in reviews]))

def update_data(review_data, total):
    query = f'''
        UNWIND {review_data} AS d
        MATCH (s)-[r:reviewed_by]->(e) WHERE id(s) = d.start and id(e) = d.end
        SET r += {{review:d.review, decision:d.decision}}
        RETURN r.review
    '''
    result = rq.make_request(query, total)
@background
def update_offset(offset):
    reviews = get_review_info(page_size, offset)
    review_data = get_reviews_formatted(reviews)
    update_data(review_data, offset + page_size )


def update_review_by():
    cnt = 0
    offset = 0
    while offset<1100000:
        cnt +=1
        offset += page_size
        update_offset(offset)
def main():
    update_review_by()

if __name__ == '__main__':
    main()
