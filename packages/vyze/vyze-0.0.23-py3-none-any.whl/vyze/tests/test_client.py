# import datetime
#
# from src import vyze
#
#
# def test_client_1():
#
#     universe = vyze.load_universe_from_api('test_universe', url='http://localhost:9150/')
#     print(str(universe.get_model('base.object/').fields[0]))
#
#     vy_client = vyze.Client(url='http://localhost:9131/access/')
#
#     # space_manager = vyze.UserSpaceManager('http://localhost:9150/')
#     # space_manager.login('julian', 'goalfoev8')
#     # vy_client.set_space_manager(space_manager)
#
#     space_token = vyze.parse_space_token('7e2a3bf22657aa37be2daa8868804d029966325641df7015831e85bf82ef0abbffffff010000000000000000eb5ae463000000001ca29c4747cb1ca50c3e4d2cd016053b91c6a7fb')
#     vy_client.register_space_token(space_token)
#
#     ids = vy_client.get_specials(universe.resolve('test'))
#     print(ids)
#
#     obj = vy_client.create_object(universe.resolve('test'), 'hello')
#     print(obj)
#
#     vy_client.set_name(obj['id'], f'test: {datetime.datetime.now()}')
#     print(vy_client.get_name(obj['id']))
