import pyeureka.const as c


class PyEurekaValidationError(Exception):
    pass


class PyEurekaInternalValidationError(Exception):
    pass


def validate_instance_definition(instance_definition):
    for needed in c.EUREKA_INSTANCE_DEFINITION['needed']:
        if needed not in instance_definition:
            raise PyEurekaValidationError("{} is necessary".format(needed))
    for part in c.EUREKA_INSTANCE_DEFINITION['needed-with-default']:
        if part[0] not in instance_definition:
            if part[1] == c.EUREKA_DEFAULT_SAME_AS:
                instance_definition[part[0]] = instance_definition[part[2]]
            elif part[1] == c.EUREKA_DEFAULT_VALUE:
                instance_definition[part[0]] = part[2]
            else:
                raise PyEurekaInternalValidationError(
                    "on {} - unknown symbol {}".format(part[0], part[1]))
    for part in c.EUREKA_INSTANCE_DEFINITION['transformations']:
        if part[0] in instance_definition and part[1](instance_definition[part[0]]):
            instance_definition[part[0]] = part[2](
                instance_definition[part[0]])
    return {'instance': instance_definition}
