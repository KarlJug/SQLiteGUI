from DB.QueryDAO import QueryDAO


class Delete:

    @staticmethod
    def separate_numbers(str_nums):
        num = ''
        nums = []
        for i in range(0, len(str_nums)):

            if i == len(str_nums) - 1 and str_nums[i].isdigit():
                num += str_nums[i]
                nums.append(int(num))

            elif str_nums[i].isdigit():
                num += str_nums[i]

            elif str_nums[i] == ' ':
                pass

            else:
                nums.append(int(num))
                num = ''

        return nums

    @staticmethod
    def integer_type(action, queryDAO):

        match action:
            case 1:
                try:
                    value = Delete.separate_numbers(input("Sisesta numberid: "))
                    queryDAO.deleteWHERE(value)
                except ValueError as error:
                    print("Error: " + str(error))

