﻿use ms_toollib::*;
use pyo3::prelude::*;

#[pyclass(name = "MinesweeperBoard")]
pub struct PyMinesweeperBoard {
    pub core: MinesweeperBoard,
}

#[pymethods]
impl PyMinesweeperBoard {
    #[new]
    pub fn new(board: Vec<Vec<i32>>) -> PyMinesweeperBoard {
        let c = MinesweeperBoard::new(board.clone());
        PyMinesweeperBoard {
            core: c,
        }
    }
    pub fn step(&mut self, e: &str, pos: (usize, usize)) {
        self.core.step(e, pos).unwrap();
    }
    pub fn step_flow(&mut self, operation: Vec<(&str, (usize, usize))>) {
        self.core.step_flow(operation).unwrap();
    }
    #[getter]
    fn get_game_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.game_board.clone())
    }
    #[getter]
    fn get_left(&self) -> PyResult<usize> {
        Ok(self.core.left)
    }
    #[getter]
    fn get_right(&self) -> PyResult<usize> {
        Ok(self.core.right)
    }
    #[getter]
    fn get_chording(&self) -> PyResult<usize> {
        Ok(self.core.chording)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.ces)
    }
    #[getter]
    fn get_flag(&self) -> PyResult<usize> {
        Ok(self.core.flag)
    }
    #[getter]
    fn get_solved3BV(&self) -> PyResult<usize> {
        Ok(self.core.solved3BV)
    }
}

#[pyclass(name = "AvfVideo")]
pub struct PyAvfVideo {
    pub core: AvfVideo,
}

#[pymethods]
impl PyAvfVideo {
    #[new]
    pub fn new(file_name: &str) -> PyAvfVideo {
        let c = AvfVideo::new(file_name);
        PyAvfVideo {
            core: c,
        }
    }
    pub fn parse_video(&mut self) {
        self.core.parse_video().unwrap();
    }
    pub fn analyse(&mut self) {
        self.core.analyse();
    }
    pub fn analyse_for_features(&mut self, controller: Vec<&str>) {
        self.core.analyse_for_features(controller);
    }
    #[getter]
    fn get_bbbv(&self) -> PyResult<usize> {
        Ok(self.core.static_params.bbbv)
    }
    #[getter]
    fn get_openings(&self) -> PyResult<usize> {
        Ok(self.core.static_params.openings)
    }
    #[getter]
    fn get_islands(&self) -> PyResult<usize> {
        Ok(self.core.static_params.islands)
    }
    #[getter]
    fn get_hizi(&self) -> PyResult<usize> {
        Ok(self.core.static_params.hizi)
    }
    #[getter]
    fn get_cell0(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell0)
    }
    #[getter]
    fn get_cell1(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell1)
    }
    #[getter]
    fn get_cell2(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell2)
    }
    #[getter]
    fn get_cell3(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell3)
    }
    #[getter]
    fn get_cell4(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell4)
    }
    #[getter]
    fn get_cell5(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell5)
    }
    #[getter]
    fn get_cell6(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell6)
    }
    #[getter]
    fn get_cell7(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell7)
    }
    #[getter]
    fn get_cell8(&self) -> PyResult<usize> {
        Ok(self.core.static_params.cell8)
    }
    #[getter]
    fn get_r_time(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.r_time)
    }
    #[getter]
    fn get_bbbv_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.bbbv_s)
    }
    #[getter]
    fn get_stnb(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.stnb)
    }
    #[getter]
    fn get_rqp(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.rqp)
    }
    #[getter]
    fn get_lefts(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.lefts)
    }
    #[getter]
    fn get_rights(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.rights)
    }
    #[getter]
    fn get_chordings(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.chordings)
    }
    #[getter]
    fn get_clicks(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.clicks)
    }
    #[getter]
    fn get_flags(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.flags)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.dynamic_params.ces)
    }
    #[getter]
    fn get_lefts_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.lefts_s)
    }
    #[getter]
    fn get_rights_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.rights_s)
    }
    #[getter]
    fn get_chordings_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.chordings_s)
    }
    #[getter]
    fn get_clicks_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.clicks_s)
    }
    #[getter]
    fn get_ces_s(&self) -> PyResult<f64> {
        Ok(self.core.dynamic_params.ces_s)
    }
    #[getter]
    fn get_events_len(&self) -> PyResult<usize> {
        Ok(self.core.events.len())
    }
    pub fn events_time(&self, index: usize) -> PyResult<f64> {
        Ok(self.core.events[index].time)
    }
    pub fn events_mouse(&self, index: usize) -> PyResult<String> {
        Ok(self.core.events[index].mouse.clone())
    }
    pub fn events_x(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.events[index].x)
    }
    pub fn events_y(&self, index: usize) -> PyResult<u16> {
        Ok(self.core.events[index].y)
    }
    pub fn events_useful_level(&self, index: usize) -> PyResult<u8> {
        Ok(self.core.events[index].useful_level)
    }
    pub fn events_posteriori_game_board(&self, index: usize) -> PyResult<PyGameBoard> {
        let mut t = PyGameBoard::new(self.core.mine_num);
        t.set_core(self.core.events[index].posteriori_game_board.clone());
        Ok(t)
    }
    pub fn events_comments(&self, index: usize) -> PyResult<String> {
        Ok(self.core.events[index].comments.clone())
    }
}

#[pyclass(name = "GameBoard")]
pub struct PyGameBoard {
    pub core: GameBoard,
}

impl PyGameBoard {
    fn set_core(&mut self, value: GameBoard) {
        self.core = value;
    }
}

#[pymethods]
impl PyGameBoard {
    #[new]
    pub fn new(mine_num: usize) -> PyGameBoard {
        let c = GameBoard::new(mine_num);
        PyGameBoard {
            core: c,
        }
    }
    #[setter]
    fn set_game_board(&mut self, board: Vec<Vec<i32>>) {
        self.core.set_game_board(&board);
    }
    #[getter]
    fn get_poss(&mut self) -> PyResult<Vec<Vec<f64>>> {
        Ok(self.core.get_poss().to_vec())
    }
    #[getter]
    fn get_basic_not_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_basic_not_mine().to_vec())
    }
    #[getter]
    fn get_basic_is_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_basic_is_mine().to_vec())
    }
    #[getter]
    fn get_enum_not_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_enum_not_mine().to_vec())
    }
    #[getter]
    fn get_enum_is_mine(&mut self) -> PyResult<Vec<(usize, usize)>> {
        Ok(self.core.get_enum_is_mine().to_vec())
    }
}







