namespace IntCodeComputer
{
    public class Computer
    {
        public int Execute(int[] input_data)
        {    
            int program_counter = 0;

            while (program_counter + 3 < input_data.Length)
            {
                int opcode = input_data[program_counter];

                if (opcode == 99)
                    break;

                int input1ptr = input_data[program_counter + 1];
                int input1 = input_data[input1ptr];

                int input2ptr = input_data[program_counter + 2];
                int input2 = input_data[input2ptr];

                int output = 0;
                if (opcode == 1)  //ADD
                    output = input1 + input2;
                else if (opcode == 2)  //MULTIPLY
                    output = input1 * input2;

                int output_ptr = input_data[program_counter + 3];
                input_data[output_ptr] = output;

                program_counter += 4;
            }        

            return input_data[0];
        }
    }
}