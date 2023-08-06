#define PY_SSIZE_T_CLEAN
#include "Python.h"

#define True 1
#define False 0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "routiner.h"

char routine[7][13][9][30];

int teacher_n, subject_n, type_n;
struct teacher *t_a;
struct day_t *dt_a;
struct subject *s_a;
struct type *ty_a;
struct section *sec_a;

char periods[8][10] = {"first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"};
char days[6][10] = {"sunday", "monday", "tuesday", "wednesday", "thursday", "friday"}; 

static PyObject *t_a_c(PyObject *self, PyObject *args) {
    static int t_n;
    if(!PyArg_ParseTuple(args, "i", &t_n)) {
        return NULL;
    }
    t_a = calloc(t_n, sizeof(struct teacher));
    teacher_n = t_n;
    dt_a = calloc(t_n * 6 , sizeof(struct day_t));
    return PyLong_FromLong(1);
}

static PyObject *t_init(PyObject *self, PyObject *args) {
    int id, i;
    const char *sub, *ini;
    if(!PyArg_ParseTuple(args, "i(iss)", &i, &id, &sub, &ini)) {
        return NULL;
    }
    (t_a+i)->id = id;
    strcpy((t_a+i)->sub, sub);
    strcpy((t_a+i)->ini, ini);
    return PyLong_FromLong(1);
}

static PyObject *t_fin(PyObject *self, PyObject *args) {
    int prs[8];
    int nt, nd, i;
    const char *day;
    if(!PyArg_ParseTuple(args,"ii(iiiiiiii)s", &nd, &nt, &prs[0], &prs[1], &prs[2], &prs[3], &prs[4], &prs[5], &prs[6], &prs[7], &day)) {
        return NULL;
    }
    (dt_a+(nt*6)+nd)->t_id = (t_a+nt)->id;;
    strcpy((dt_a+(nt*6)+nd)->day_name, (char*)day);
    for(i = 0;i < 8;i++) {
        if(prs[i]) {
            (dt_a+(nt*6)+nd)->periods[i] = prs[i];
        }
    }
    return PyLong_FromLong(1);
}

static PyObject *s_a_c(PyObject *self, PyObject *args) {
    int s_n;
    if(!PyArg_ParseTuple(args, "i", &s_n)) {
        return NULL;
    }
    s_a = calloc(s_n, sizeof(struct subject));
    subject_n = s_n;
    return PyLong_FromLong(1);
}

static PyObject *s_init(PyObject *self, PyObject *args) {
    int id, i, n_prds;
    const char *sub_name, *grade;
    if(!PyArg_ParseTuple(args, "i(issi)", &i, &id, &sub_name, &grade, &n_prds)) {
        return NULL;
    }
    (s_a+i)->id = id;
    strcpy((s_a+i)->sub_name, (char*)sub_name);
    strcpy((s_a+i)->grade, (char*)grade);
    (s_a+i)->n_period = n_prds;
    return PyLong_FromLong(1);
}

static PyObject *sec_c(PyObject *self, PyObject *args)  {
    int sec_n;
    if(!PyArg_ParseTuple(args, "i", &sec_n)) {
        return NULL;
    }
    sec_a = calloc(sec_n, sizeof(struct section));
    return PyLong_FromLong(1);
}

static PyObject *sec_init(PyObject *self, PyObject *args) {
    int id, i;
    const char *sec, *grade;
    if(!PyArg_ParseTuple(args, "i(iss)", &i, &id, &sec, &grade)) {
        return NULL;
    }
    (sec_a+i)->id = id;
    strcpy((sec_a+i)->sec_name, sec);
    strcpy((sec_a+i)->grade, grade);
    return PyLong_FromLong(1);
}

static PyObject *sec_s(PyObject *self, PyObject *args) {
    int nsec, ns, sub_id;
    if(!PyArg_ParseTuple(args, "iii", &ns, &nsec, &sub_id)) {
        return NULL;
    }
    (sec_a+nsec)->sub[ns] = sub_id;
    return PyLong_FromLong(1);
}

static PyObject *ty_a_c(PyObject *self, PyObject *args) {
    static int ty_n;
    if(!PyArg_ParseTuple(args, "i", &ty_n)) {
        return NULL;
    }
    type_n = ty_n;
    ty_a = calloc(ty_n, sizeof(struct type));
    return PyLong_FromLong(1);
}

static PyObject *ty_init(PyObject *self, PyObject *args) {
    int id, sec_id, s_id, n_prds, is_pr, i;
    if(!PyArg_ParseTuple(args, "i(iiiii)", &i, &id, &sec_id, &s_id, &n_prds, &is_pr)) {
        return NULL;
    }
    (ty_a+i)->id = id;
    (ty_a+i)->sec_id = sec_id;
    (ty_a+i)->s_id = s_id;
    (ty_a+i)->n_prds = n_prds;
	(ty_a+i)->n_prds_o = n_prds;
    (ty_a+i)->is_practical = is_pr;
    return PyLong_FromLong(1);
}

static PyObject *ty_t(PyObject *self, PyObject *args) {
    int i, ty_i, t_id;
    if(!PyArg_ParseTuple(args, "iii", &i, &ty_i, &t_id)) {
        return NULL;
    }
    (ty_a+ty_i)->t_id[i] = t_id;
    return PyLong_FromLong(1);
}

void load_data() {
    int i, j, k;
    for(i = 0;i < 7;i++) {
        for(j = 0;j < 13;j++) {
            for(k = 0;k < 9;k++) {
                strcpy(routine[i][j][k], "");
            }
        }
    }
    for(i = 1;i < 7;i++) {
        strcpy(routine[i][0][0], days[i-1]);
    }

    static char class[10];
    for(i = 1;i < 13;i++) {
        strcpy(class, (sec_a+i-1)->sec_name);
        strcat(class, "_");
        strcat(class, (sec_a+i-1)->grade);
        strcpy(routine[0][i][0], class);
    }
    
    for(i = 1;i < 9;i++) {
        strcpy(routine[0][0][i], periods[i-1]);
    }
}

static PyObject *mk_rt(PyObject *self, PyObject *args) {
    load_data();
    
    int day, sec, prd, l, type_id;
    int *prac_per_day;
    int* ty_id;
    ty_id = calloc(20, sizeof(int));

    struct subject* s;
    struct teacher* t;
    struct type* ty;

    char period[30];

    for(day = 1;day < 7;day++) {
        prac_per_day = calloc(12, sizeof(int));
        for(prd = 8;prd > 0;prd--) {
            for(sec = 1;sec < 13;sec++) {

                if(strcmp(routine[day][sec][prd], "") != 0) {
                    continue;
                }

                get_periods_dps(ty_id, day, (sec_a+sec-1)->id, prd, *(prac_per_day+sec-1));
                filter_teachers(ty_id, day, sec, prd);

                type_id = get_gpc(ty_id, day, sec);
                ty = get_type(type_id); 
                
                if(ty == NULL) {
                    continue;
                }
                
                s = get_subject(ty->s_id);
                strcpy(period, s->sub_name);

                if(ty->is_practical) {  
                    for(l = 0;l < 4;l++) {
                        if(!check_practical_teacher(ty->t_id[l], day, prd, period)) {
                            break;
                        }
                    }        
                    strcpy(routine[day][sec][prd], period);
                    strcpy(routine[day][sec][prd-1], period);

                    *(prac_per_day+sec-1) = True;
					
                    ty->n_prds -= 2;
                } else {
                    t = get_teacher(ty->t_id[0]);
                    strcat(period, "+");
                    strcat(period, t->ini);
                    cut_day_t(t->id, day, prd);

                    strcpy(routine[day][sec][prd], period);               
                    ty->n_prds--;
                }
                strcpy(period, "");
            }
            cut_all_day_t(day, prd);
        }
        free(prac_per_day);
    }

	//Generating python dictionary using 4 dimensional array.
    
    static PyObject *rt;
    static PyObject *d;
    static PyObject *section;
    static PyObject *text;
    
    rt = PyDict_New();
    for(day = 1;day < 7;day++) {
        d = PyDict_New();
        for(sec = 1;sec < 13;sec++) {
            section = PyDict_New();
            for(prd = 1;prd < 9;prd++) {
                text = PyUnicode_FromString(routine[day][sec][prd]);
                PyDict_SetItemString(section, routine[0][0][prd], text);
            }
            PyDict_SetItemString(d, routine[0][sec][0], section);
        }
        PyDict_SetItemString(rt, routine[day][0][0], d);
    }

    return rt;
}

struct teacher* get_teacher(int id) {
    for(int i = 0;i < 30;i++) {
        if((t_a+i)->id == id) {
            return &t_a[i];
        }
    }
    return NULL;
}

struct subject* get_subject(int id) {
    for(int i = 0;i < subject_n;i++) {
        if((s_a+i)->id == id) {
            return &s_a[i];
        }
    }
    return NULL;
}

struct type* get_type(int id) {
    for(int i = 0;i < type_n;i++) {
        if((ty_a+i)->id == id) {
            return &ty_a[i];
        }
    }
    return NULL;
}

void cut_day_t(int t_id, int d, int k) {
    for(int i = 0;i < teacher_n * 6;i++) {
        if((dt_a+i)->t_id == t_id && strcmp((dt_a+i)->day_name, days[d-1]) == 0) {
            (dt_a+i)->periods[k-1] = False;
            break;
        }
    }
}

void cut_all_day_t(int day, int prd) {
    for(int i = 0;i< teacher_n * 6;i++) {
        if(strcmp((dt_a+i)->day_name, days[day-1]) == 0) {
            (dt_a+i)->periods[prd-1] = False;
        }
    }
}

void get_type_sec(int *ty, int sec_id) {
    int c = 0, i;
    for(i = 0;i < type_n;i++) {
        if((ty_a+i)->sec_id == sec_id && (ty_a+i)->n_prds != 0) {
            *(ty+c) = (ty_a+i)->id;
            c++;
        }
    }
    for(i = c;i < 20;i++) {
        *(ty+i) = 0;
    }
}

unsigned int is_day_period_able(int id, int d, int p) {
    for(int i = 0;i < (teacher_n * 6);i++) {
        if((dt_a+i)->t_id == id && (strcmp((dt_a+i)->day_name, days[d-1]) == 0) && (dt_a+i)->periods[p-1]) {
            return True;
        }
    }
    return False;
}

void get_teachers_dp(int *ty_id, int d, int p, int prac_per_day){
    int c = 0, i, j;
    unsigned int _is_day_avl1, _is_day_avl2;

    struct type *ty;
    struct teacher *t;

    for(i = 0;i < 20;i++) {
        _is_day_avl1 = False;
        _is_day_avl2 = False;

        ty = get_type(*(ty_id+i));
        if(ty == NULL) {
            continue;
        }

        if(ty->is_practical) {
            if(!prac_per_day) {
                for(j = 0;j < 4;j++) {
                    t = get_teacher(ty->t_id[j]);
                    if(t == NULL) {
                        break;
                    }

                    if(!is_day_period_able(t->id, d, p)) {
                        _is_day_avl1 = False;
                        break;
                    } else {
                        _is_day_avl1 = True;
                    }

                    if(p == 1 || p == 6) {
                        _is_day_avl2 =  False;
                        break;
                    }  else {
                        if(!is_day_period_able(t->id, d, p-1)) {
                            _is_day_avl2 = False;
                            break;
                        } else {
                            _is_day_avl2 = True;
                        }
                    }
                }
            } 
        } else {
            t = get_teacher(ty->t_id[0]);
            _is_day_avl1 = is_day_period_able(t->id, d, p);
            _is_day_avl2 = True;
        }

        if(_is_day_avl1 && _is_day_avl2) {
            *(ty_id+c) = ty->id;
            c++; 
        }
    }

    for(i = c;i < 20;i++) {
        *(ty_id+i) = 0;
    }
}

void get_periods_dps(int *dest, int d, int sec_id, int p, int prac_per_day) {
    get_type_sec(dest, sec_id);
    get_teachers_dp(dest, d, p, prac_per_day);
}

void filter_teachers(int *ty_id, int d, int sec, int p) {
    int i, j, c = 0;
    unsigned int _is_done;

    char period[30];

    struct type* ty;
    struct subject* s;
    struct teacher* t;

    for(i = 0;i < 20;i++) {

        ty = get_type(*(ty_id+i));

        if(ty == NULL) {
            continue;
        }

        if(!(ty->is_practical)) {
            _is_done = False;
            for(j = 8;j > p;j--) {
                s = get_subject(ty->s_id);
                t = get_teacher(ty->t_id[0]);
                strcpy(period, s->sub_name);
                strcat(period, "+");
                strcat(period, t->ini);
                if((strcmp(routine[d][sec][j], period) == 0)) {  
                    _is_done = True;
                    break;
                }
            }
            if(!_is_done) {
                *(ty_id+c) = ty->id;
                c++;
            }

        } else {
            *(ty_id+c) = ty->id;
            c++;
        }
    }
    
    for(i = c;i < 20;i++) {
        *(ty_id+i) = 0;
    }
}

int get_gpc(int *ty_id, int d, int sec) {
    int index = 0, i, j;
    double pc[20][4], _pc;
    struct type *ty;
    struct teacher *t;

    for(i = 0;i < 20;i++) {
        ty = get_type(*(ty_id+i));
        for(j = 0;j < 4;j++) {
            if(ty == NULL) {
                pc[i][j] = 0;
                continue;
            }
            t = get_teacher(ty->t_id[j]);
            if(t != NULL) {
                pc[i][j] = calculate_pc(ty->id, ty->t_id[j], d, sec);
            } else {
                pc[i][j] = 0;
            }
        }
    }
		
	
	_pc = pc[0][0];
	
	for(i = 0;i < 20;i++) {
		for(j = 0;j < 4;j++) {
			if(pc[i][j] > _pc) {
				_pc = pc[i][j];
				index = i;
			}
		}
	}	

    return *(ty_id+index);
}

double calculate_pc(int ty_id, int t_id, int d, int sec) {
    unsigned short Ns = 0, Na = 0, Nd = 0, Nt = 0, Nts = 0, Nsd = 0, Nty = 0, i, j;
    double Ac, Sc, Dc, Tc, TSc, SDc;

    struct type *ty;
    struct subject *s;
	struct teacher *t;
    
    ty = get_type(ty_id);
    s = get_subject(ty->s_id);

    for(i = 0;i < type_n;i++) {
        if((ty_a+i)->sec_id == ty->sec_id && (ty_a+i)->s_id == ty->s_id) {
            Nt += (ty_a+i)->n_prds;
			Nty++;
        }


        for(j = 0;j < 4;j++) {

            if((ty_a+i)->t_id[j] == t_id) {
                Ns += (ty_a+i)->n_prds;
                break;
            }
        }
    }
	if(Ns == 0) {
		return 0;
	}
    for(i = 1;i < 7;i++) {
        for(j = 1;j < 9;j++) {
            if(is_day_period_able(t_id, i, j)) {
                Na++;
            }
        }
    }
	if(Na == 0) {
		return 0;
	}
	
	j = 0;	

	for(i = 0;i < 4;i++) {
		t = get_teacher(ty->t_id[i]);
		if(t != NULL) {
			j++;
		}
	}
	
	char *subject = calloc(11, sizeof(char));

    for(i = 1;i < 9;i++) {
        if(is_day_period_able(t_id, d, i)) {
            Nd++;
        }
		subject = strtok(routine[d][sec][i], "+");
		if(strcmp(subject, s->sub_name) == 0) {
			Nsd++;
		}
    }

	Nts = ty->n_prds;

	if(Nd == 0 || Nt == 0 || Nts == 0 || Nsd == 0 || Nty == 0) {
		return 0;
	}
	
	if(ty->is_practical) {
		Nt *= j;
	}

	Ac = (double)Na;
	Sc = (double)Ns;
	Dc = 8/(double)Nd;
	SDc = (double)Nty/Nsd;

    Tc = (double)Nt/(s->n_period);
	TSc = (double)Nts/ty->n_prds_o;

    return (Ac * Sc * Tc * Dc * TSc * SDc);
}

unsigned int check_practical_teacher(int id, int d, int p, char* _period) {
    struct teacher* t;
    t = get_teacher(id);
    if(t == NULL) {
        return False;
    }
    cut_day_t(t->id, d, p);
    cut_day_t(t->id, d, p-1);
    strcat(_period, "+");
    strcat(_period, t->ini);
    return True;
}

static PyMethodDef RoutinerMethods[] = {
    {"create_teachers", t_a_c, METH_VARARGS, "(n)"},
    {"teacher_init", t_init, METH_VARARGS, "(index, (id, subject, intials)"},
    {"teacher_days", t_fin, METH_VARARGS, "(index, teacher_index, (pr1, pr2, .., pr8), day)"},
    {"create_subjects", s_a_c, METH_VARARGS, "(n)"},
    {"subject_init", s_init, METH_VARARGS, "(index, (id, subject, grade, n_periods, is_pr))"},
    {"create_section", sec_c, METH_VARARGS, "(n)"},
    {"section_init", sec_init, METH_VARARGS, "(index, (id, section, grade))"},
    {"section_subjects", sec_s, METH_VARARGS, "(index, section_index, subject_id)"},
    {"create_types", ty_a_c, METH_VARARGS, "(n)"},
    {"type_init", ty_init, METH_VARARGS, "(index, (type, teacher_n, section_id, subject_id, num_periods, is_practical))"},
    {"type_teachers", ty_t, METH_VARARGS, "(index, type_index, teacher_id)"},
    {"make_routine", mk_rt, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef routinermodule = {
    PyModuleDef_HEAD_INIT,
    "pyroutiner",
    NULL,
    -1,
    RoutinerMethods
};

PyMODINIT_FUNC PyInit_pyroutiner(void) {
    return PyModule_Create(&routinermodule);
}
