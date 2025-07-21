import inspect
from functools import wraps
from uuid import UUID
from typing import Optional, get_args, get_origin

# def type_assert(*ty_args, **ty_kwargs):
#     def decorate(func):
#         if not __debug__:
#             return func
#         sig = inspect.signature(func)
#         bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             bound_values = sig.bind(*args, **kwargs)
#             for name, value in bound_values.arguments.items():
#                 if name in bound_types:
#                     expected_type = bound_types[name]
#                     if get_origin(expected_type) is Optional:
#                         if value is None:
#                             continue
#                         expected_type = get_args(expected_type)[0]
#                     if expected_type is UUID:
#                         if not isinstance(value, (UUID, str)):
#                             raise TypeError(f'Argument {name} must be UUID or str')
#                         try:
#                             if isinstance(value, str):
#                                 bound_values.arguments[name] = UUID(value)
#                         except ValueError:
#                             raise TypeError(f'Argument {name} is not a valid UUID string')
#                     elif not isinstance(value, expected_type):
#                         raise TypeError(f'Argument {name} must be {expected_type}')
#             return func(*bound_values.args, **bound_values.kwargs)
#         return wrapper
#     return decorate


from typing import Optional, get_origin, get_args, Union
from uuid import UUID
import inspect
from functools import wraps


def type_assert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)

            for name, value in bound_values.arguments.items():
                if name not in bound_types:
                    continue

                expected_type = bound_types[name]

                # Пропускаем None для Optional
                if value is None and get_origin(expected_type) is Union:
                    continue

                # Обработка UUID (включая Optional[UUID])
                if (expected_type is UUID or
                        (get_origin(expected_type) is Union and UUID in get_args(expected_type))):

                    if isinstance(value, str):
                        try:
                            bound_values.arguments[name] = UUID(value)
                        except ValueError:
                            raise TypeError(f'Argument {name} is not a valid UUID string')
                    elif not isinstance(value, UUID):
                        raise TypeError(f'Argument {name} must be UUID or str')

                # Общая проверка для не-Optional типов
                elif get_origin(expected_type) is None and not isinstance(value, expected_type):
                    raise TypeError(f'Argument {name} must be {expected_type}')

            return func(*bound_values.args, **bound_values.kwargs)

        return wrapper

    return decorate

# в будущем добавить неизменяемости данным(user.phone, например)(не про декоратор)
# добавить фиксацию обновленных полей
# Обновляем только допустимые поля
#     valid_fields = {'rating', 'notes', 'tags'}  # пример допустимых полей для обновления
#     for key, value in fields_data.items():
#         if key in valid_fields and hasattr(book_record, key):
#             setattr(book_record, key, value)
# добавить проверку на дубликаты
# добавить     def to_dict(self):
#         return {
#             "id": str(self.publisher_id),
#             "name": self.name
#         } для классов вызов return publisher.to_dict()
# добавить проверку  на наличие автора в create_book