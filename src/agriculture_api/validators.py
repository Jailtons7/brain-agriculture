from django.core.exceptions import ValidationError


ERROR_MESSAGE = {
    "document": "Invalid document. Please enter a valid CPF or CNPJ. "
                "Important: only numbers are allowed."
}


def validate_cpf(cpf: str) -> str:
    if not cpf.isdigit() or len(cpf) != 11:
        raise ValidationError(ERROR_MESSAGE)

    if cpf == cpf[0] * 11:
        # same digit eg.: 11111111111
        raise ValidationError(ERROR_MESSAGE)

    sum1 = sum(int(digit) * weight for digit, weight in zip(cpf[:9], range(10, 1, -1)))
    digit1 = (sum1 * 10 % 11) % 10

    sum2 = sum(int(digit) * weight for digit, weight in zip(cpf[:9] + str(digit1), range(11, 1, -1)))
    digit2 = (sum2 * 10 % 11) % 10

    if cpf[-2:] != f"{digit1}{digit2}":
        raise ValidationError(ERROR_MESSAGE)

    return cpf


def validate_cnpj(cnpj: str) -> str:
    if not cnpj.isdigit() or len(cnpj) != 14:
        raise ValidationError(ERROR_MESSAGE)

    if cnpj == cnpj[0] * 14:
        raise ValidationError(ERROR_MESSAGE)

    def calculate_digit(cnpj_partial, weights):
        total = sum(int(digit) * weight for digit, weight in zip(cnpj_partial, weights))
        remainder = total % 11
        return '0' if remainder < 2 else str(11 - remainder)

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digit1 = calculate_digit(cnpj[:12], weights1)

    weights2 = [6] + weights1
    digit2 = calculate_digit(cnpj[:12] + digit1, weights2)

    if cnpj[-2:] != digit1 + digit2:
        raise ValidationError(ERROR_MESSAGE)

    return cnpj


def validate_document(document: str):
    if len(document) == 11:
        return validate_cpf(cpf=document)
    elif len(document) == 14:
        return validate_cnpj(cnpj=document)
    else:
        raise ValidationError(ERROR_MESSAGE)


def validate_areas(arable_area: float, vegetation_area: float, total_area: float):
    total_sub_areas = (arable_area or 0) + (vegetation_area or 0)
    if total_sub_areas > (total_area or 0):
        raise ValidationError({
            "total_area": "A soma das áreas agricultável e de vegetação não pode "
                          "exceder a área total da propriedade."
        })
