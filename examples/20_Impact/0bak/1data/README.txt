������https://blog.csdn.net/lammps_jiayou/article/details/118099651
1. ���ɵ���Fe����
   atomsk --create fcc 3.615 Cu Cu.xsf
2. �����ྦྷ�ڵ��ļ���polycrystal.txt ��
   box 150 150 20     #cell size
   random 10          #random 20 grain
3. ���ɶྦྷ�ļ�final.lmp
   atomsk --polycrystal Cu.xsf polycrystal.txt final.lmp -wrap
4. ʹ���ı��༭����final.lmp�ļ����������޸ģ�
   ��1��ԭ��������1�ָ�Ϊ3��
        3 atom types
   ��2�����Ni��Crԭ��Ħ������
        Masses   
        1  55.84500000    # Fe 
        2  58.69          # Ni 
        3  51.96          #Cr
5. �滻ԭ�����ɺϽ�ṹ
   ��дin�ļ�����lammps��ʹ���滻ԭ�ӷ���������Feԭ�Ӱ��ձ����滻ΪNi��Cr���õ��Ͻ�ྦྷ�ṹ��
   in�ļ��ű����£�
   units           metal 
   boundary        p p p 
   atom_style      atomic 
   timestep        0.001 
   neighbor        0.2 bin 
   read_data       final.lmp 
   set             type 1 type/ratio 2 0.33 8793 
   set             type 1 type/ratio 3 0.5 56332 
   write_data      Fe-Ni-Cr.data

                     
