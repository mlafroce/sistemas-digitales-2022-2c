library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
  generic(
    N : integer := 8
  );
  port (
    clk : in std_logic;
    count : out unsigned(N downto 0);
    enabled : in std_logic;
    reset : in std_logic
  );
end entity; 

architecture behaviour of counter is
  signal count_reg : unsigned(N downto 0) := ( others => '0');
begin

  count <= count_Reg;
  
  process (clk) is
  begin
    if rising_edge(clk) then
      if reset = '1' then
        count_Reg <= to_unsigned(0, N);
      elsif enabled = '1' then
          count_Reg <= count_Reg + to_unsigned(1, N);
      end if;
    end if;
  end process;

end architecture;
